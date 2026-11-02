import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pickle

# ============================================================
# 1. LOAD MODEL
# ============================================================
with open("model_tree.pkl", "rb") as file:
    model = pickle.load(file)

# ============================================================
# 2. INPUT DATA BARU
# ============================================================
usia = float(input("Masukkan usia: "))
berat = float(input("Masukkan berat badan (kg): "))

# ============================================================
# 3. DATA BARU
# ============================================================
data_baru = [[usia, berat]]

# ============================================================
# 4. PREDIKSI
# ============================================================
prediksi = model.predict(data_baru)

# ============================================================
# 5. HASIL
# ============================================================
print("\n===================================")
print("HASIL PREDIKSI")
print("===================================")
print("Usia                    :", usia)
print("Berat Badan             :", berat, "kg")
print("Prediksi Tekanan Darah  :", round(prediksi[0], 2))