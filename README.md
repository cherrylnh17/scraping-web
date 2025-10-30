# Fashion Studio Scraper ETL

Proyek ini adalah pipeline **ETL (Extract, Transform, Load)** dalam Python yang dirancang untuk melakukan scraping data produk dari situs e-commerce fiksi **Fashion Studio** (`https://fashion-studio.dicoding.dev/`). Data mentah kemudian diolah dan dimuat ke berbagai tujuan penyimpanan.

---

## Struktur Proyek

├── main.py                # Skrip utama untuk menjalankan pipeline ETL
├── requirements.txt       # Daftar dependensi Python
├── .env                   # File konfigurasi (tidak di-commit, lihat .gitignore)
├── .gitignore             # Daftar file/direktori yang diabaikan Git
├── utils/
│   ├── extract.py         # Modul untuk tahap Extract (Scraping)
│   ├── transform.py       # Modul untuk tahap Transform (Pembersihan & Olah Data)
│   └── load.py            # Modul untuk tahap Load (Penyimpanan ke CSV/DB/Google Sheets)
└── tests/
    ├── test_extract.py    # Unit test untuk extract.py
    ├── test_transform.py  # Unit test untuk transform.py
    └── test_load.py       # Unit test untuk load.py


---

## Fitur Utama

| Tahapan | Modul | Deskripsi |
| :--- | :--- | :--- |
| **Extract** | `utils/extract.py` | Menggunakan `requests` dan `BeautifulSoup` untuk melakukan scraping data produk (Title, Price, Rating, Colors, Size, Gender, dan timestamp) dari halaman web. |
| **Transform** | `utils/transform.py` | Membersihkan data, menormalisasi rating, menghitung jumlah warna, dan **mengonversi harga dari USD ke Rupiah** (default rate **16.000 IDR/USD**). |
| **Load** | `utils/load.py` | Mendukung penyimpanan data bersih ke: **CSV** (default), **Google Sheets**, dan **PostgreSQL**. |

---

## Instalasi

1.  **Clone repositori** dan **buat virtual environment** (disarankan).
2.  **Instal dependensi** dari `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

---

## Konfigurasi Environment

Buat file `.env` di root proyek untuk mengelola kredensial. File ini otomatis dimuat oleh `main.py`.

```env
# File konfigurasi environment (.env)
DATABASE_URL=postgresql://user:password@host:port/dbname # URL koneksi PostgreSQL (jika ingin menyimpan ke DB)
SPREADSHEET_ID=123A-XYZ... # ID Google Sheets target (jika ingin menyimpan ke Google Sheets)
CREDS_PATH=google-sheets-api.json # Path ke Service Account JSON untuk Google Sheets API

Catatan: Pastikan CREDS_PATH dan .env masuk dalam .gitignore untuk keamanan.


Penggunaan
Jalankan skrip utama main.py menggunakan argumen argparse.

Contoh Dasar (Scraping dan Simpan ke CSV)
Akan men-scrape 50 halaman dan menyimpan output ke products.csv.

python main.py
# Atau dengan spesifikasi:
python main.py --pages 10 --output data_harian.csv


Tentu, ini adalah kode untuk file README.md yang telah saya buat berdasarkan seluruh file yang Anda unggah sebelumnya. Anda bisa langsung menyalinnya:

Markdown

# Fashion Studio Scraper ETL

Proyek ini adalah pipeline **ETL (Extract, Transform, Load)** dalam Python yang dirancang untuk melakukan scraping data produk dari situs e-commerce fiksi **Fashion Studio** (`https://fashion-studio.dicoding.dev/`). Data mentah kemudian diolah dan dimuat ke berbagai tujuan penyimpanan.

---

## Struktur Proyek

. ├── main.py # Skrip utama untuk menjalankan pipeline ETL ├── requirements.txt # Daftar dependensi Python ├── .env # File konfigurasi (tidak di-commit, lihat .gitignore) ├── .gitignore # Daftar file/direktori yang diabaikan Git ├── utils/ │ ├── extract.py # Modul untuk tahap Extract (Scraping) │ ├── transform.py # Modul untuk tahap Transform (Pembersihan & Olah Data) │ └── load.py # Modul untuk tahap Load (Penyimpanan ke CSV/DB/Google Sheets) └── tests/ ├── test_extract.py # Unit test untuk extract.py ├── test_transform.py # Unit test untuk transform.py └── test_load.py # Unit test untuk load.py


---

## Fitur Utama

| Tahapan | Modul | Deskripsi |
| :--- | :--- | :--- |
| **Extract** | `utils/extract.py` | Menggunakan `requests` dan `BeautifulSoup` untuk melakukan scraping data produk (Title, Price, Rating, Colors, Size, Gender, dan timestamp) dari halaman web. |
| **Transform** | `utils/transform.py` | Membersihkan data, menormalisasi rating, menghitung jumlah warna, dan **mengonversi harga dari USD ke Rupiah** (default rate **16.000 IDR/USD**). |
| **Load** | `utils/load.py` | Mendukung penyimpanan data bersih ke: **CSV** (default), **Google Sheets**, dan **PostgreSQL**. |

---

## Instalasi

1.  **Clone repositori** dan **buat virtual environment** (disarankan).
2.  **Instal dependensi** dari `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

---

## Konfigurasi Environment

Buat file `.env` di root proyek untuk mengelola kredensial. File ini otomatis dimuat oleh `main.py`.

```env
# File konfigurasi environment (.env)
DATABASE_URL=postgresql://user:password@host:port/dbname # URL koneksi PostgreSQL (jika ingin menyimpan ke DB)
SPREADSHEET_ID=123A-XYZ... # ID Google Sheets target (jika ingin menyimpan ke Google Sheets)
CREDS_PATH=google-sheets-api.json # Path ke Service Account JSON untuk Google Sheets API
Catatan: Pastikan CREDS_PATH dan .env masuk dalam .gitignore untuk keamanan.

Penggunaan
Jalankan skrip utama main.py menggunakan argumen argparse.

Contoh Dasar (Scraping dan Simpan ke CSV)
Akan men-scrape 50 halaman dan menyimpan output ke products.csv.

Bash

python main.py
# Atau dengan spesifikasi:
python main.py --pages 10 --output data_harian.csv
Menyimpan ke PostgreSQL dan Google Sheets
Gunakan flag --postgres dan/atau sediakan --spreadsheet ID.

# Menjalankan scraping, simpan ke CSV, dan upload ke PostgreSQL (tabel 'products')
python main.py --pages 50 --postgres

# Menjalankan scraping, simpan ke CSV, dan upload ke Google Sheets
python main.py --spreadsheet 123A-XYZ...

Argumen Command Line

Argumen	Tipe	Default	Deskripsi
--pages	int	50	Jumlah halaman yang akan di-scrape.
--output	str	products.csv	Nama file output CSV.
--spreadsheet	str	None	Google Sheets ID (menimpa nilai di .env).
--creds	str	google-sheets-api.json	Path ke file service account JSON (menimpa nilai di .env).
--postgres	action="store_true"	False	Flag untuk mengaktifkan penyimpanan ke PostgreSQL.
--postgres_table	str	products	Nama tabel di PostgreSQL.


Menjalankan Unit Test
Proyek ini dilengkapi dengan unit test menggunakan Pytest.

Menjalankan semua tes

python -m pytest tests

Menjalankan tes dengan laporan coverage

coverage run -m pytest tests
coverage report -m
