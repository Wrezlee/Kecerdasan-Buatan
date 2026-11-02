import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ==========================
# LOAD MODEL
# ==========================

NAMA_MODEL = "taufiqdp/indonesian-sentiment"

# Urutan label model pre-trained: negatif, netral, positif
KELAS = ["negative", "neutral", "positive"]

tokenizer = AutoTokenizer.from_pretrained(NAMA_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(NAMA_MODEL)
model.eval()

# ==========================
# INPUT KALIMAT
# ==========================

kalimat = input("Masukkan kalimat : ")

# ==========================
# PREDIKSI
# ==========================

inputs = tokenizer(
    kalimat,
    return_tensors="pt",
    truncation=True,
    max_length=128
)

with torch.no_grad():
    logits = model(**inputs).logits

prob = torch.softmax(logits, dim=-1)[0]
idx = int(prob.argmax())

print("\n" + "=" * 50)
print("HASIL PREDIKSI")
print("=" * 50)

print("Kalimat  :", kalimat)
print("Sentimen :", KELAS[idx])
print("Keyakinan: {:.2%}".format(prob[idx].item()))