import os
import re
import pandas as pd
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ==========================
# KONFIGURASI
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NAMA_FILE = "MBG_Merge.csv"   # GANTI dengan nama file dataset MBG
KOLOM_TEKS = "full_text"

NAMA_MODEL = "taufiqdp/indonesian-sentiment"

# Urutan label model pre-trained: negatif, netral, positif
KELAS = ["negative", "neutral", "positive"]

# Isi angka (misal 2000) untuk mencoba cepat, atau None untuk semua data
JUMLAH_DATA = None

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(os.path.join(BASE_DIR, NAMA_FILE))
df = df[[KOLOM_TEKS]].dropna().drop_duplicates().reset_index(drop=True)

if JUMLAH_DATA:
    df = df.sample(n=min(JUMLAH_DATA, len(df)), random_state=42).reset_index(drop=True)

print("Jumlah tweet:", len(df))

def bersihkan_ringan(text):
    text = str(text)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

teks = df[KOLOM_TEKS].apply(bersihkan_ringan).tolist()

# ==========================
# LOAD MODEL PRE-TRAINED
# ==========================

print("Memuat model", NAMA_MODEL, "...")
tokenizer = AutoTokenizer.from_pretrained(NAMA_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(NAMA_MODEL)
model.eval()

# ==========================
# PELABELAN (BATCH)
# ==========================

UKURAN_BATCH = 32
hasil = []

for i in range(0, len(teks), UKURAN_BATCH):
    batch = teks[i:i + UKURAN_BATCH]
    inputs = tokenizer(
        batch,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )
    with torch.no_grad():
        logits = model(**inputs).logits
    hasil.extend(logits.argmax(dim=-1).tolist())

    if (i // UKURAN_BATCH) % 10 == 0:
        print(f"Diproses {min(i + UKURAN_BATCH, len(teks))}/{len(teks)}")

df["sentiment"] = [KELAS[i] for i in hasil]

print("\nDistribusi sentimen:")
print(df["sentiment"].value_counts())

# ==========================
# SIMPAN
# ==========================

df.to_csv(os.path.join(BASE_DIR, "mbg_berlabel.csv"), index=False)
print("\nTersimpan: mbg_berlabel.csv")