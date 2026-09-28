import matplotlib

# Backend untuk menampilkan grafik di Windows
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from inference import penaksir
from membership import harga

# =====================================
# INPUT USER
# =====================================

print("=" * 45)
print("SISTEM FUZZY PENAKSIR HARGA RUMAH")
print("=" * 45)

luas_input = float(
    input("Luas bangunan (30-300 m2): ")
)

lokasi_input = float(
    input("Skor lokasi (0-100): ")
)

umur_input = float(
    input("Umur bangunan (0-40 tahun): ")
)

# =====================================
# INPUT KE SISTEM FUZZY
# =====================================

penaksir.input['luas'] = luas_input
penaksir.input['lokasi'] = lokasi_input
penaksir.input['umur'] = umur_input

# =====================================
# PROSES INFERENSI
# =====================================

penaksir.compute()

hasil = penaksir.output['harga']

# =====================================
# OUTPUT
# =====================================

print("\n=============================================")
print("HASIL FUZZY MAMDANI")
print("=============================================")

print("Luas bangunan :", luas_input, "m2")
print("Skor lokasi   :", lokasi_input)
print("Umur bangunan :", umur_input, "tahun")
print("Taksiran Harga: Rp %.2f juta" % hasil)

if hasil < 700:
    kategori = "MURAH"
elif hasil < 1400:
    kategori = "SEDANG"
else:
    kategori = "MAHAL"

print("Kategori      :", kategori)

# =====================================
# VISUALISASI HARGA
# =====================================

harga.view(sim=penaksir)

plt.show()
