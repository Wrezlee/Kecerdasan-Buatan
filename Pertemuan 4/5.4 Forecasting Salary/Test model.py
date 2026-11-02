# ============================================================
# TEST MODEL SALARY
# ============================================================
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
experience = float(input("Masukkan Years of Experience: "))

# ============================================================
# 3. PREDIKSI
# ============================================================
data_baru = [[experience]]
prediksi = model.predict(data_baru)

# ============================================================
# 4. HASIL
# ============================================================
print("\n===================================")
print("HASIL PREDIKSI")
print("===================================")
print("Years of Experience :", experience)
print("Prediksi Salary     :", round(prediksi[0], 2))