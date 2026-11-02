import os
import re
import string
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================
# KONFIGURASI (SESUAIKAN)
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NAMA_FILE = "mbg_berlabel.csv"   # nama file dataset
KOLOM_TEKS = "full_text"                   # kolom berisi kalimat
KOLOM_LABEL = "sentiment"             # kolom berisi label

# Jika label berupa angka/kode, petakan di sini. Contoh:
# LABEL_MAP = {0: "negative", 1: "neutral", 2: "positive"}
LABEL_MAP = {}

# ==========================
# PREPROCESSING
# ==========================

def preprocessing(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ==========================
# LOAD DATA
# ==========================

path = os.path.join(BASE_DIR, NAMA_FILE)

if NAMA_FILE.lower().endswith((".xlsx", ".xls")):
    df = pd.read_excel(path)
else:
    df = pd.read_csv(path)

df = df[[KOLOM_TEKS, KOLOM_LABEL]].dropna()

if LABEL_MAP:
    df[KOLOM_LABEL] = df[KOLOM_LABEL].map(LABEL_MAP)
    df = df.dropna()

df[KOLOM_LABEL] = df[KOLOM_LABEL].astype(str).str.strip().str.lower()
df["clean"] = df[KOLOM_TEKS].apply(preprocessing)
df = df[df["clean"] != ""]

print("Dataset:", df.shape)
print(df[KOLOM_LABEL].value_counts())

# ==========================
# SPLIT TRAIN / TEST (80:20)
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    df["clean"],
    df[KOLOM_LABEL],
    test_size=0.2,
    random_state=42,
    stratify=df[KOLOM_LABEL]
)

print("Data train:", X_train.shape[0])
print("Data test :", X_test.shape[0])

# ==========================
# TF-IDF
# ==========================

tfidf = TfidfVectorizer(max_features=5000)

X_train = tfidf.fit_transform(X_train)
X_test = tfidf.transform(X_test)

# ==========================
# MLP CLASSIFIER
# ==========================

model = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    activation="relu",
    solver="adam",
    learning_rate_init=0.001,
    max_iter=300,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================
# EVALUASI
# ==========================

y_pred = model.predict(X_test)

print("=" * 50)
print("HASIL EVALUASI")
print("=" * 50)

print("Accuracy :", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred, zero_division=0))

# ==========================
# SIMPAN MODEL
# ==========================

joblib.dump(model, os.path.join(BASE_DIR, "model_sentimen.pkl"))
joblib.dump(tfidf, os.path.join(BASE_DIR, "tfidf.pkl"))

print("Model berhasil disimpan.")