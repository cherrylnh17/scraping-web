import os
import argparse
from utils import extract, transform, load
from dotenv import load_dotenv

load_dotenv()

def run(args):
    df_raw = extract.scrape_all(pages=args.pages)
    df_clean = transform.transform(df_raw)
    csv_path = load.save_csv(df_clean, path=args.output)
    print(f"[load] Saved CSV: {csv_path}")

    # Google Sheets
    spreadsheet_id = args.spreadsheet or os.environ.get("SPREADSHEET_ID")
    creds_path = os.environ.get("CREDS_PATH", args.creds)

    if spreadsheet_id:
        try:
            res = load.save_to_google_sheets(df_clean, spreadsheet_id=spreadsheet_id, creds_json=creds_path)
            print(f"[load] Saved to Google Sheets: {res}")
        except Exception as e:
            print(f"[load] warning: failed to save to Google Sheets: {e}")

    # PostgreSQL
    if args.postgres:
        try:
            load.save_to_postgres(df_clean, table_name=args.postgres_table)
            print("[load] Saved to Postgres")
        except Exception as e:
            print(f"[load] warning: failed to save to Postgres: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=50)
    parser.add_argument("--output", type=str, default="products.csv")
    parser.add_argument("--spreadsheet", type=str, help="Google Sheets ID", default=None)
    parser.add_argument("--creds", type=str, help="Path ke file service account JSON", default="google-sheets-api.json")
    parser.add_argument("--postgres", action="store_true", help="Simpan ke PostgreSQL")
    parser.add_argument("--postgres_table", type=str, default="products")
    args = parser.parse_args()
    run(args)
