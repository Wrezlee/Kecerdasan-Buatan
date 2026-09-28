import matplotlib.pyplot as plt
from inference import speed
from membership import kecepatan

# =====================================
# INPUT USER
# =====================================

print("=" * 45)
print("SISTEM FUZZY PENENTUAN KECEPATAN")
print("=" * 45)

jarak = float(input("Jarak kendaraan depan (0-100 m): "))
lalu = float(input("Kepadatan lalu lintas (0-100%): "))
jalan = float(input("Kondisi jalan (0-10): "))

speed.input['jarak'] = jarak
speed.input['lalu_lintas'] = lalu
speed.input['jalan'] = jalan

# =====================================
# PROSES INFERENSI
# =====================================

speed.compute()
hasil = speed.output['kecepatan']

# =====================================
# OUTPUT
# =====================================

print("\n" + "=" * 45)
print("HASIL")
print("=" * 45)
print(f"Jarak         : {jarak} meter")
print(f"Lalu lintas   : {lalu}%")
print(f"Kondisi jalan : {jalan}")
print(f"Kecepatan     : {hasil:.2f} km/jam")

if hasil < 40:
    kategori = "LAMBAT"
elif hasil < 80:
    kategori = "SEDANG"
else:
    kategori = "CEPAT"

print(f"Kategori      : {kategori}")

# =====================================
# VISUALISASI
# =====================================

kecepatan.view(sim=speed)
plt.show()
