import os
import re
import string
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def preprocessing(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ==========================
# LOAD MODEL
# ==========================

model = joblib.load(os.path.join(BASE_DIR, "model_sentimen.pkl"))
tfidf = joblib.load(os.path.join(BASE_DIR, "tfidf.pkl"))

# ==========================
# INPUT KALIMAT
# ==========================

kalimat = input("Masukkan kalimat : ")

# ==========================
# PREDIKSI
# ==========================

kalimat_tfidf = tfidf.transform([preprocessing(kalimat)])
hasil = model.predict(kalimat_tfidf)

print("\n" + "=" * 50)
print("HASIL PREDIKSI")
print("=" * 50)

print("Kalimat  :", kalimat)
print("Sentimen :", hasil[0])