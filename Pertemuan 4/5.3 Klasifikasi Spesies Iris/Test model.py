import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pickle

# ============================================================
# 1. LOAD MODEL
# ============================================================
with open("model_tree.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
target_names = model_data["target_names"]

# ============================================================
# 2. INPUT DATA BARU
# ============================================================
sepal_length = float(input("Sepal length (cm): "))
sepal_width = float(input("Sepal width (cm): "))
petal_length = float(input("Petal length (cm): "))
petal_width = float(input("Petal width (cm): "))

# ============================================================
# 3. DATA BARU
# ============================================================
data_baru = [[sepal_length, sepal_width, petal_length, petal_width]]

# ============================================================
# 4. PREDIKSI
# ============================================================
prediksi = model.predict(data_baru)

# ============================================================
# 5. HASIL
# ============================================================
hasil = target_names[prediksi[0]]

print("\n===================================")
print("HASIL PREDIKSI")
print("===================================")
print("Prediksi Species :", hasil)