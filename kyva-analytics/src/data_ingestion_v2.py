"""
Tiny ingestion stub for KYVA project (safe for first runs).

What it does (for now):
- Looks for CSV files in ../data/
- Loads the selected CSV with pandas
- Saves a curated Parquet copy to ../data/curated/ (creates folder if needed)
- Prints a tiny summary

Usage (from repo root):
    python kyva-analytics/src/data_ingestion.py
"""

from pathlib import Path
import pandas as pd

# Paths
SRC_DIR = Path(__file__).resolve().parent
DATA_DIR = SRC_DIR.parent / "data"
CURATED_DIR = DATA_DIR / "curated"
CURATED_DIR.mkdir(parents=True, exist_ok=True)

def list_csvs():
    return sorted(DATA_DIR.glob("*.csv"))

def load_data(csv_path: Path) -> pd.DataFrame:
    # Adjust options if your file is large or has specific encoding
    return pd.read_csv(csv_path, low_memory=False)

def save_curated(df: pd.DataFrame, out_path: Path):
    # Parquet is compact + fast; requires pyarrow
    df.to_parquet(out_path, index=False)

def main():
    csv_files = list_csvs()
    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}. Drop your sample CSV there and re-run.")
        return

    # Pick the first CSV by default (simple baby step); you can change this later
    csv_path = csv_files[0]
    print(f"Loading: {csv_path.name}")

    df = load_data(csv_path)

    # Minimal summary
    print(f"Rows: {len(df):,}  |  Columns: {len(df.columns)}")
    print("Columns:", list(df.columns)[:10], ("..." if len(df.columns) > 10 else ""))

    # Save a curated parquet snapshot
    out_path = CURATED_DIR / (csv_path.stem + ".parquet")
    save_curated(df, out_path)
    print(f"Saved curated parquet → {out_path.relative_to(SRC_DIR.parent)}")

if __name__ == "__main__":
    main()
