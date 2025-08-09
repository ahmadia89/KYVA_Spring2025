"""
Tiny Streamlit app for KYVA (first demo).

What it does:
- Looks for a curated Parquet file in ../data/curated/ (preferred)
- If none exists, falls back to any CSV in ../data/
- Lets you pick a file, shows shape + first rows, and simple column info
"""

from pathlib import Path
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent / "data"
CURATED_DIR = DATA_DIR / "curated"

st.set_page_config(page_title="KYVA Analytics (Demo)", layout="wide")
st.title("KYVA Attendance & Engagement — Demo Viewer")

# Find files
parquets = sorted(CURATED_DIR.glob("*.parquet")) if CURATED_DIR.exists() else []
csvs = sorted(DATA_DIR.glob("*.csv"))

files = [*parquets, *csvs]
if not files:
    st.warning(f"No data found. Put a CSV in `{DATA_DIR}` or run the ingestion script first.")
    st.stop()

choice = st.selectbox("Choose a file to preview:", files, format_func=lambda p: p.name)

# Load
if choice.suffix.lower() == ".parquet":
    df = pd.read_parquet(choice)
else:
    df = pd.read_csv(choice, low_memory=False)

# Basic info
st.write(f"**File:** `{choice.name}`")
st.write(f"**Rows:** {len(df):,}   **Columns:** {len(df.columns)}")

# Peek
st.subheader("Preview (first 25 rows)")
st.dataframe(df.head(25), use_container_width=True)

# Quick column summary
with st.expander("Column summary"):
    st.write(pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "non_null": df.notna().sum(),
        "nulls": df.isna().sum()
    }))

st.caption("Tip: run the ingestion script to generate a curated Parquet version for faster loading.")
