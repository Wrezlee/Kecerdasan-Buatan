import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pickle

# ============================================================
# 1. LOAD MODEL
# ============================================================
with open("model_tree.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
le_usia = model_data["le_usia"]
le_aktivitas = model_data["le_aktivitas"]
le_target = model_data["le_target"]

# ============================================================
# 2. INPUT DATA BARU
# ============================================================
usia = input("Masukkan usia (Muda/Tua): ").strip().lower()
aktivitas = input("Masukkan aktivitas fisik (Aktif/Tidak Aktif): ").strip().lower()

# ============================================================
# 3. SESUAIKAN DENGAN LABEL ASLI
# ============================================================
mapping_usia = {label.lower(): label for label in le_usia.classes_}
mapping_aktivitas = {label.lower(): label for label in le_aktivitas.classes_}

if usia not in mapping_usia:
    print("\nInput usia tidak valid.")
    print("Pilihan:", list(mapping_usia.keys()))
    exit()

if aktivitas not in mapping_aktivitas:
    print("\nInput aktivitas tidak valid.")
    print("Pilihan:", list(mapping_aktivitas.keys()))
    exit()

usia_asli = mapping_usia[usia]
aktivitas_asli = mapping_aktivitas[aktivitas]

# ============================================================
# 4. ENCODING
# ============================================================
usia_encoded = le_usia.transform([usia_asli])[0]
aktivitas_encoded = le_aktivitas.transform([aktivitas_asli])[0]

data_baru = [[usia_encoded, aktivitas_encoded]]

# ============================================================
# 5. PREDIKSI
# ============================================================
prediksi = model.predict(data_baru)

# ============================================================
# 6. HASIL
# ============================================================
hasil = le_target.inverse_transform(prediksi)

print("\n===================================")
print("HASIL PREDIKSI")
print("===================================")
print("Usia               :", usia_asli)
print("Aktivitas Fisik     :", aktivitas_asli)
print("Risiko Hipertensi  :", hasil[0])