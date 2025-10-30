import os
import pandas as pd
from pathlib import Path

class LoadError(Exception):
    """Custom exception error tahap Load."""
    pass


def save_csv(df: pd.DataFrame, path: str = "products.csv") -> str:
    """Simpan DataFrame ke file CSV."""
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        raise LoadError(f"Failed to save CSV: {e}")
    return path


def save_to_google_sheets(df: pd.DataFrame, spreadsheet_id: str, creds_json: str = "google-sheets-api.json") -> str:
    """Upload DataFrame ke Google Sheets."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except Exception as e:
        raise LoadError(f"Google Sheets libraries not installed: {e}")

    if not Path(creds_json).exists():
        raise LoadError(f"Service account JSON not found: {creds_json}")

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = service_account.Credentials.from_service_account_file(creds_json, scopes=scopes)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    values = [list(df.columns)] + df.values.tolist()
    body = {"values": values}

    try:
        res = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
    except Exception as e:
        raise LoadError(f"Failed to write to Google Sheets: {e}")
    return str(res)


def save_to_postgres(df: pd.DataFrame, table_name: str = "products") -> None:
    """Simpan DataFrame ke tabel PostgreSQL menggunakan SQLAlchemy."""
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise LoadError("DATABASE_URL environment variable not set")

    try:
        from sqlalchemy import create_engine
    except Exception as e:
        raise LoadError(f"SQLAlchemy not installed: {e}")

    try:
        engine = create_engine(DATABASE_URL)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
    except Exception as e:
        raise LoadError(f"Failed to write to Postgres: {e}")
