import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# GANTI dengan nama file hasil unduhan dari Kaggle (.csv atau .xlsx)
NAMA_FILE = "MBG_Merge.csv"

path = os.path.join(BASE_DIR, NAMA_FILE)

if NAMA_FILE.lower().endswith((".xlsx", ".xls")):
    df = pd.read_excel(path)
else:
    # Jika kolom tidak terbaca benar, coba ganti sep=";" atau sep="\t"
    df = pd.read_csv(path)

print("Ukuran data :", df.shape)
print("\nNama kolom  :", list(df.columns))
print("\n5 baris pertama:")
print(df.head())

print("\nKolom yang kemungkinan label (nilai unik sedikit):")
for kolom in df.columns:
    n = df[kolom].nunique()
    if n <= 10:
        print(f"\n{kolom} ({n} nilai unik)")
        print(df[kolom].value_counts(dropna=False))