import matplotlib.pyplot as plt
from inference import diagnosa
from membership import risiko

# =====================================
# INPUT USER
# =====================================

print("=" * 40)
print("SISTEM FUZZY RISIKO DIABETES")
print("=" * 40)

gula_input = float(input("Gula darah (70-250 mg/dL): "))
bmi_input = float(input("BMI (15-40): "))
umur_input = float(input("Umur (15-80 tahun): "))

diagnosa.input['gula'] = gula_input
diagnosa.input['bmi'] = bmi_input
diagnosa.input['umur'] = umur_input

# =====================================
# PROSES INFERENSI
# =====================================

diagnosa.compute()
hasil = diagnosa.output['risiko']

# =====================================
# OUTPUT
# =====================================

print("\n===== HASIL =====")
print(f"Gula Darah : {gula_input}")
print(f"BMI        : {bmi_input}")
print(f"Umur       : {umur_input}")
print(f"Risiko     : {hasil:.2f}")

if hasil < 40:
    kategori = "Risiko Rendah"
elif hasil < 70:
    kategori = "Risiko Sedang"
else:
    kategori = "Risiko Tinggi"

print(f"Kategori   : {kategori}")

# =====================================
# VISUALISASI
# =====================================

risiko.view(sim=diagnosa)
plt.show()
