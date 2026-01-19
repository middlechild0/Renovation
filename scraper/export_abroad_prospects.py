#!/usr/bin/env python3
"""
Export abroad (non-Africa) prospects to CSV.
Output filename: abroad_prospects.csv in the project directory.
"""
import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "businesses.db")
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abroad_prospects.csv")

# Countries to exclude (Africa focus)
EXCLUDED_COUNTRIES = {
    "Kenya", "Nigeria", "Ghana", "South Africa", "Egypt", "Morocco", "Uganda", "Tanzania", "Ethiopia",
}

# Countries we explicitly want to keep (Europe/USA/Canada/Australia)
PREFERRED_COUNTRIES = {
    "United States", "USA", "Canada", "Australia", "United Kingdom", "France", "Germany", "Deutschland",
    "Netherlands", "Spain", "Italy", "Austria", "Czech Republic", "Ireland", "Switzerland", "Belgium",
    "Portugal", "Sweden", "Norway", "Denmark", "Finland", "Poland",
}


def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    df = pd.read_sql_query("SELECT * FROM businesses", conn)
    if df.empty:
        raise RuntimeError("No businesses found to export.")
    mask_not_africa = ~df['country'].isin(EXCLUDED_COUNTRIES)
    mask_preferred = df['country'].isin(PREFERRED_COUNTRIES)
    filtered = df[mask_not_africa & mask_preferred]
    filtered.to_csv(OUTPUT, index=False)
    print(f"Exported {len(filtered)} abroad prospects to {OUTPUT}")


if __name__ == "__main__":
    main()
