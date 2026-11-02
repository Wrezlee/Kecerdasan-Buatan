import joblib

# ==========================
# LOAD MODEL
# ==========================

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model_sentimen.pkl"))
tfidf = joblib.load(os.path.join(BASE_DIR, "tfidf.pkl"))

# ==========================
# INPUT KALIMAT
# ==========================

kalimat = input("Masukkan kalimat : ")

# ==========================
# TF-IDF
# ==========================

kalimat_tfidf = tfidf.transform([kalimat])

# ==========================
# PREDIKSI
# ==========================

hasil = model.predict(kalimat_tfidf)

print("\n" + "=" * 50)
print("HASIL PREDIKSI")
print("=" * 50)

print("Kalimat :", kalimat)
print("Sentimen :", hasil[0])

