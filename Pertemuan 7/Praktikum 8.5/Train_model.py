import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================
# LOAD DATA
# ==========================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

train = pd.read_csv(os.path.join(BASE_DIR, "train_preprocess_ori.tsv"), sep="\t")
test = pd.read_csv(os.path.join(BASE_DIR, "valid_preprocess.tsv"), sep="\t")

X_train = train["text"]
y_train = train["sentiment"]

X_test = test["text"]
y_test = test["sentiment"]

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
print(classification_report(y_test, y_pred))

# ==========================
# SIMPAN MODEL
# ==========================

joblib.dump(model, os.path.join(BASE_DIR, "model_sentimen.pkl"))
joblib.dump(tfidf, os.path.join(BASE_DIR, "tfidf.pkl"))