import matplotlib.pyplot as plt
from inference import simulasi
from membership import kelembapan, suhu, penyiraman

# =====================================
# INPUT
# =====================================

kelembapan_input = float(input("Masukkan kelembapan tanah (%): "))
suhu_input = float(input("Masukkan suhu udara (°C): "))

# =====================================
# PROSES
# =====================================

simulasi.input['kelembapan'] = kelembapan_input
simulasi.input['suhu'] = suhu_input
simulasi.compute()

# =====================================
# OUTPUT
# =====================================

hasil = simulasi.output['penyiraman']

print("\n===================================")
print("HASIL FUZZY MAMDANI")
print("===================================")
print(f"Kelembapan Tanah : {kelembapan_input:.1f}%")
print(f"Suhu Udara       : {suhu_input:.1f}°C")
print(f"Lama Penyiraman  : {hasil:.2f} menit")

penyiraman.view(sim=simulasi)
plt.show()
