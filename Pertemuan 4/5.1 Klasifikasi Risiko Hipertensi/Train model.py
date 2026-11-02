import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd

df = pd.read_excel("Dataset_Hipertensi.xlsx")

print("=" * 50)
print("DATASET RISIKO HIPERTENSI")
print("=" * 50)
print(df)
print("\nUkuran Data :", df.shape)

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================
from sklearn.preprocessing import LabelEncoder

# Encoding Usia
le_usia = LabelEncoder()
df["Usia"] = le_usia.fit_transform(df["Usia"])

# Encoding Aktivitas Fisik
le_aktivitas = LabelEncoder()
df["Aktivitas Fisik"] = le_aktivitas.fit_transform(df["Aktivitas Fisik"])

# Encoding target
le_target = LabelEncoder()
df["Risiko Hipertensi"] = le_target.fit_transform(df["Risiko Hipertensi"])

print("=" * 50)
print("DATA SETELAH PREPROCESSING")
print("=" * 50)
print(df)

print("\nEncoding Usia:")
print(dict(zip(le_usia.classes_, le_usia.transform(le_usia.classes_))))

print("\nEncoding Aktivitas Fisik:")
print(dict(zip(le_aktivitas.classes_, le_aktivitas.transform(le_aktivitas.classes_))))

print("\nEncoding Risiko Hipertensi:")
print(dict(zip(le_target.classes_, le_target.transform(le_target.classes_))))

# ============================================================
# 3. APPLY DECISION TREE CLASSIFIER
# ============================================================
from sklearn.tree import DecisionTreeClassifier

X = df[["Usia", "Aktivitas Fisik"]]
y = df["Risiko Hipertensi"]

model = DecisionTreeClassifier(criterion="entropy", random_state=42)
model.fit(X, y)

# ============================================================
# VISUALISASI DECISION TREE
# ============================================================
from sklearn.tree import export_text

aturan = export_text(model, feature_names=["Usia", "Aktivitas Fisik"])
print(aturan)

# ============================================================
# 4. EVALUASI
# ============================================================
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Prediksi
y_pred = model.predict(X)

# Evaluasi
accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred)
recall = recall_score(y, y_pred)
cm = confusion_matrix(y, y_pred)

print("=" * 50)
print("HASIL EVALUASI")
print("=" * 50)
print("Accuracy :", round(accuracy, 4))
print("Precision :", round(precision, 4))
print("Recall :", round(recall, 4))
print("\nConfusion Matrix:")
print(cm)

# ============================================================
# 5. SIMPAN MODEL TREE
# ============================================================
import pickle

model_data = {
    "model": model,
    "le_usia": le_usia,
    "le_aktivitas": le_aktivitas,
    "le_target": le_target
}

with open("model_tree.pkl", "wb") as file:
    pickle.dump(model_data, file)

print("\nModel berhasil disimpan...")