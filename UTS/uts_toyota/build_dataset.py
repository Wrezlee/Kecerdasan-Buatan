"""Ekstrak baris TOYOTA (A. WHOLESALES) per bulan dari PDF GAIKINDO "BY BRAND"
lalu simpan ke data/toyota_wholesales.csv. Setiap tahun diverifikasi terhadap
total yang tercetak di PDF."""
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

UPLOADS = Path("/mnt/user-data/uploads")
FILES = {
    2022: "2-gaikindo_brand_data_jandec2022_rev2.pdf",
    2023: "2_GAIKINDO_brand_data_jandec2023_1.pdf",
    2024: "2_GAIKINDO_brand_data_jandec2024.pdf",
    2025: "2_GAIKINDO_brand_data_jandec2025_REV.pdf",
    2026: "2_GAIKINDO_brand_data_jansep2026.pdf",
}
OUT = Path(__file__).parent / "data" / "toyota_wholesales.csv"


def to_int(tok: str) -> int:
    return int(tok.replace(".", "").replace(",", ""))


def toyota_wholesales(pdf: Path):
    text = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    # baris pertama "1 TOYOTA ..." ada di bagian A. WHOLESALES
    for line in text.splitlines():
        m = re.match(r"\s*1\s+TOYOTA\s+(.*)$", line)
        if m:
            toks = m.group(1).split()
            vals, total_tok = [], None
            # 12 kolom bulan (angka atau '-'), lalu total tahun, lalu persen
            months = toks[:12]
            total_tok = toks[12]
            vals = [0 if t == "-" else to_int(t) for t in months]
            return vals, to_int(total_tok)
    raise ValueError(f"baris TOYOTA tidak ditemukan di {pdf}")


rows = []
for year, fname in FILES.items():
    vals, printed_total = toyota_wholesales(UPLOADS / fname)
    n = 9 if year == 2026 else 12  # 2026 baru sampai September
    vals = vals[:n]
    s = sum(vals)
    ok = "OK" if s == printed_total else "BEDA!"
    print(f"{year}: {n} bulan, jumlah={s:,}  total_tercetak={printed_total:,}  -> {ok}")
    if s != printed_total:
        sys.exit(f"Verifikasi gagal untuk {year}")
    for i, v in enumerate(vals, start=1):
        rows.append({"bulan": f"{year}-{i:02d}", "penjualan": v})

df = pd.DataFrame(rows)
OUT.parent.mkdir(exist_ok=True)
df.to_csv(OUT, index=False)
print(f"\nTersimpan: {OUT}  ({len(df)} baris, {df.bulan.iloc[0]} s.d. {df.bulan.iloc[-1]})")
print(df.penjualan.describe().round(1).to_string())
