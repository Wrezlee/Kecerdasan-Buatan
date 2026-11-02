import os
import pandas as pd
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================
# KONFIGURASI
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NAMA_MODEL = "taufiqdp/indonesian-sentiment"

# Urutan label model pre-trained: negatif, netral, positif
KELAS = ["negative", "neutral", "positive"]

# File data berlabel asli (bukan masked)
FILE_DATA = "valid_preprocess.tsv"

# ==========================
# LOAD DATA
# ==========================

def baca_data(nama_file):
    df = pd.read_csv(
        os.path.join(BASE_DIR, nama_file),
        sep="\t",
        header=None,
        names=["text", "sentiment"]
    )
    # Baris header (jika ada) dan label kosong ikut terbuang di sini
    df = df[df["sentiment"].isin(KELAS)].reset_index(drop=True)
    return df

data = baca_data(FILE_DATA)

X_test = data["text"].astype(str).tolist()
y_test = data["sentiment"].tolist()

print("Dataset evaluasi:", data.shape)
print(data["sentiment"].value_counts())

# ==========================
# LOAD MODEL PRE-TRAINED
# ==========================

print("\nMemuat model", NAMA_MODEL, "...")
tokenizer = AutoTokenizer.from_pretrained(NAMA_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(NAMA_MODEL)
model.eval()

# ==========================
# PREDIKSI (BATCH)
# ==========================

def prediksi(daftar_teks, ukuran_batch=16):
    hasil = []
    for i in range(0, len(daftar_teks), ukuran_batch):
        batch = daftar_teks[i:i + ukuran_batch]
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
    return [KELAS[i] for i in hasil]

y_pred = prediksi(X_test)

# ==========================
# EVALUASI
# ==========================

print("=" * 50)
print("HASIL EVALUASI")
print("=" * 50)

print("Accuracy :", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred, labels=KELAS))

print("\nClassification Report")
print(classification_report(y_test, y_pred, labels=KELAS, zero_division=0))

# ==========================
# SIMPAN HASIL
# ==========================

data["prediksi"] = y_pred
data.to_csv(os.path.join(BASE_DIR, "hasil_prediksi.csv"), index=False)

print("Hasil prediksi disimpan ke hasil_prediksi.csv")