import os
import pandas as pd

MASTER_PATH = os.path.join("data", "processed", "anuncios_master.parquet")

if not os.path.exists(MASTER_PATH):
    raise SystemExit("Master file not found. Run 05_build_master.py first.")

df = pd.read_parquet(MASTER_PATH)

print("\n=== BASIC INFO ===")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n=== COLUMN NAMES ===")
for col in df.columns:
    print("-", col)

print("\n=== SAMPLE ROW ===")
print(df.head(1).T)

print("\n=== NON-NULL % BY COLUMN ===")
print((df.notna().mean() * 100).sort_values(ascending=False))