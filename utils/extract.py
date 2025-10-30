# utils/extract.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

BASE_URL = "https://fashion-studio.dicoding.dev/"

class ExtractError(Exception):
    pass

def scrape_page(session: requests.Session, page: int) -> pd.DataFrame:
    """
    Scrape halaman dari fashion-studio.dicoding.dev.
    
    Args:
        session (requests.Session): Session HTTP yang digunakan.
        page (int): Nomor halaman yang akan di-scrape.
    
    Returns:
        pd.DataFrame: Data produk dari halaman tersebut.
    
    Raises:
        ExtractError: Jika terjadi kegagalan HTTP atau parsing.
    """
    try:
        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}page{page}"
        
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise ExtractError(f"Failed to fetch page {page}: {e}")

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select(".collection-card") 

    rows = []
    for c in cards:
        title = c.select_one(".product-title")
        price = c.select_one(".price")
        ps = c.select(".product-details p")

        rating, colors, size, gender = None, None, None, None
        for ptag in ps:
            text = ptag.get_text(strip=True)
            if text.startswith("Rating"):
                rating = text.replace("Rating:", "").strip()
            elif "Colors" in text:
                colors = text.strip()
            elif "Size:" in text:
                size = text.replace("Size:", "").strip()
            elif "Gender:" in text:
                gender = text.replace("Gender:", "").strip()

        rows.append({
            "Title": title.get_text(strip=True) if title else None,
            "Price": price.get_text(strip=True) if price else None,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
        })

    df = pd.DataFrame(rows)
    df["timestamp"] = datetime.utcnow().isoformat()
    return df



def scrape_all(pages: int = 50, sleep: float = 1.0) -> pd.DataFrame:
    session = requests.Session()
    all_dfs = []
    for p in range(1, pages + 1):
        print(f"[extract] scraping page {p}/{pages} ...")
        try:
            df = scrape_page(session, p)
            all_dfs.append(df)
        except ExtractError as e:
            print(f"[extract] warning: {e}")
        time.sleep(sleep)
    if not all_dfs:
        raise ExtractError("No data extracted from any page")
    print("[extract] selesai scraping semua halaman")
    return pd.concat(all_dfs, ignore_index=True)
