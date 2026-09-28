import matplotlib.pyplot as plt
from inference import ac
from membership import suhu_ac

# =====================================
# INPUT USER
# =====================================

print("=" * 45)
print("SISTEM FUZZY PENGATUR SUHU AC OTOMATIS")
print("=" * 45)

suhu_input = float(input("Suhu ruangan (18-40 C): "))
orang_input = float(input("Jumlah orang (0-20): "))
lembap_input = float(input("Kelembapan (20-100%): "))

ac.input['suhu_ruangan'] = suhu_input
ac.input['jumlah_orang'] = orang_input
ac.input['kelembapan'] = lembap_input

# =====================================
# PROSES INFERENSI
# =====================================

ac.compute()
hasil = ac.output['suhu_ac']

# =====================================
# OUTPUT
# =====================================

print("\n===== HASIL =====")
print(f"Suhu ruangan : {suhu_input} C")
print(f"Jumlah orang : {orang_input}")
print(f"Kelembapan   : {lembap_input}%")
print(f"Suhu AC      : {hasil:.2f} C")

if hasil < 21:
    kategori = "DINGIN"
elif hasil < 24:
    kategori = "SEDANG"
else:
    kategori = "HANGAT"

print(f"Kategori     : {kategori}")

# =====================================
# VISUALISASI
# =====================================

suhu_ac.view(sim=ac)
plt.show()
