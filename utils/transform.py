"""
Module: transform
-----------------
Modul ini bertanggung jawab untuk melakukan tahap **Transform** dalam pipeline ETL.

Data mentah hasil scraping dari website diubah menjadi format yang bersih, 
terstruktur, dan bertipe data konsisten agar siap dimuat ke database atau file CSV.

Fungsi-fungsi utama :
- Konversi harga USD ke Rupiah
- Pembersihan format rating
- Penghitungan jumlah warna
- Normalisasi ukuran dan gender produk
- Validasi dan penghapusan data tidak valid

"""

import pandas as pd
import re


class TransformError(Exception):
    pass


def _to_rupiah(price_text: str, rate: int = 16000) -> int:
    """
    Mengonversi teks harga berformat dolar menjadi nilai integer dalam Rupiah.

    Args:
        price_text (str): Teks harga produk dalam USD.
        rate (int, optional): Nilai tukar USD ke IDR. Default = 16.000.

    Returns:
        int: Harga dalam satuan Rupiah (dibulatkan).

    Raises:
        ValueError: Jika harga kosong, tidak valid, atau "Price Unavailable".
    """
    if not price_text:
        raise ValueError("Empty price")
    price_text = price_text.strip()
    if "Price Unavailable" in price_text or "Unavailable" in price_text:
        raise ValueError("Price Unavailable")
    m = re.search(r"\$(\d+(?:[\.,]\d+)?)", price_text)
    if not m:
        raise ValueError(f"Invalid price format: {price_text}")
    val = float(m.group(1).replace(',', '.'))
    return int(round(val * rate))


def _clean_rating(r: str) -> float:
    """
    Membersihkan teks rating dan mengubahnya ke tipe float.

    Args:
        r (str): Teks rating mentah.

    Returns:
        float: Nilai rating sebagai angka desimal.

    Raises:
        ValueError: Jika rating kosong atau tidak mengandung angka valid.
    """
    if not r:
        raise ValueError("Empty rating")
    r = r.strip()
    if "Invalid" in r or not re.search(r"\d", r):
        raise ValueError("Invalid Rating")
    m = re.search(r"(\d+(?:[\.,]\d+)?)", r)
    if not m:
        raise ValueError("Invalid Rating")
    return float(m.group(1).replace(',', '.'))


def _count_colors(c: str) -> int:
    """
    Menghitung jumlah warna dari teks deskripsi warna produk.

    Args:
        c (str): Teks warna produk.

    Returns:
        int: Jumlah warna produk.

    Raises:
        ValueError: Jika nilai kosong atau tidak valid.
    """
    if c is None:
        raise ValueError("Empty colors")
    c = c.strip()
    m = re.search(r"(\d+)", c)
    if m:
        return int(m.group(1))
    parts = [p.strip() for p in re.split(r",|;", c) if p.strip()]
    if not parts:
        raise ValueError("Invalid colors")
    return len(parts)


def _clean_size(s: str) -> str:
    """
    Membersihkan teks ukuran produk.

    Args:
        s (str): Teks ukuran mentah.

    Returns:
        str: Ukuran yang sudah bersih.

    Raises:
        ValueError: Jika ukuran kosong.
    """
    if not s:
        raise ValueError("Empty size")
    s = s.strip()
    s = re.sub(r"(?i)^size[:\s]*", "", s)
    return s


def _clean_gender(g: str) -> str:
    """
    Membersihkan teks gender produk.

    Args:
        g (str): Teks gender mentah.

    Returns:
        str: Gender yang sudah bersih.

    Raises:
        ValueError: Jika gender kosong.
    """
    if not g:
        raise ValueError("Empty gender")
    g = g.strip()
    g = re.sub(r"(?i)^gender[:\s]*", "", g)
    return g


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melakukan transformasi penuh pada DataFrame hasil scraping agar siap untuk tahap Load.

    Langkah-langkah:
    1. Menghapus baris kosong atau berjudul "Unknown Product".
    2. Mengonversi harga ke Rupiah.
    3. Membersihkan dan memvalidasi rating, warna, ukuran, dan gender.
    4. Menghapus baris yang memiliki data None di kolom penting.
    5. Menghapus duplikat berdasarkan Title dan Price.
    6. Menjamin tipe data setiap kolom sesuai spesifikasi.
    7. Mengurutkan kolom sesuai format final output.

    Args:
        df (pd.DataFrame): DataFrame mentah hasil scraping.

    Returns:
        pd.DataFrame: DataFrame bersih dengan kolom:
            - Title (str)
            - Price (int, dalam Rupiah)
            - Rating (float)
            - Colors (int)
            - Size (str)
            - Gender (str)
            - timestamp

    Raises:
        TransformError: Jika DataFrame kosong.
    """
    if df.empty:
        raise TransformError("Empty DataFrame")

    df = df.copy()

    # Filter data tidak valid
    df["Title"] = df["Title"].astype(object)
    df = df[df["Title"].notna()]
    df = df[~df["Title"].str.contains("Unknown Product", na=False)]

    # Transform kolom Price
    prices, mask_keep = [], []
    for v in df["Price"].tolist():
        try:
            rup = _to_rupiah(v)
            prices.append(rup)
            mask_keep.append(True)
        except Exception:
            prices.append(None)
            mask_keep.append(False)
    df["Price"] = prices

    # Transform kolom Rating
    ratings = []
    for v in df["Rating"].tolist():
        try:
            ratings.append(_clean_rating(v))
        except Exception:
            ratings.append(None)
    df["Rating"] = ratings

    # Transform kolom Colors
    colors_parsed = []
    for v in df["Colors"].tolist():
        try:
            colors_parsed.append(_count_colors(v))
        except Exception:
            colors_parsed.append(None)
    df["Colors"] = colors_parsed

    # Transform kolom Size
    sizes = []
    for v in df["Size"].tolist():
        try:
            sizes.append(_clean_size(v))
        except Exception:
            sizes.append(None)
    df["Size"] = sizes

    # Transform kolom Gender
    genders = []
    for v in df["Gender"].tolist():
        try:
            genders.append(_clean_gender(v))
        except Exception:
            genders.append(None)
    df["Gender"] = genders

    # Drop data tidak lengkap
    df = df.dropna(subset=["Title", "Price", "Rating", "Colors", "Size", "Gender"])

    # Hapus duplikasi
    df = df.drop_duplicates(subset=["Title", "Price"])

    df = df.astype({
        "Title": str,
        "Price": int,
        "Rating": float,
        "Colors": int,
        "Size": str,
        "Gender": str
    })

    # Urutkan kolom
    cols = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    df = df[cols]

    return df.reset_index(drop=True)
