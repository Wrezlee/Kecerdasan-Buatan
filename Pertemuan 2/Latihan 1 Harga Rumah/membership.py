import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# =====================================
# RANGE VARIABEL INPUT
# =====================================

luas = ctrl.Antecedent(np.arange(30, 301, 1), 'luas')
lokasi = ctrl.Antecedent(np.arange(0, 101, 1), 'lokasi')
umur = ctrl.Antecedent(np.arange(0, 41, 1), 'umur')

# =====================================
# RANGE VARIABEL OUTPUT
# =====================================

harga = ctrl.Consequent(np.arange(100, 2001, 1), 'harga')

# =====================================
# MEMBERSHIP LUAS BANGUNAN
# Semesta 30-300 m2
# Kecil 30-100 | Sedang 80-220 | Besar 180-300
# =====================================

luas['kecil'] = fuzz.trapmf(luas.universe, [30, 30, 60, 100])
luas['sedang'] = fuzz.trimf(luas.universe, [80, 150, 220])
luas['besar'] = fuzz.trapmf(luas.universe, [180, 220, 300, 300])

# =====================================
# MEMBERSHIP LOKASI
# Semesta 0-100
# Kurang 0-45 | Strategis 35-85 | Sangat Strategis 75-100
# =====================================

lokasi['kurang'] = fuzz.trapmf(lokasi.universe, [0, 0, 25, 45])
lokasi['strategis'] = fuzz.trimf(lokasi.universe, [35, 60, 85])
lokasi['sangat'] = fuzz.trapmf(lokasi.universe, [75, 90, 100, 100])

# =====================================
# MEMBERSHIP UMUR BANGUNAN
# Semesta 0-40 tahun
# Baru 0-10 | Sedang 8-28 | Tua 25-40
# =====================================

umur['baru'] = fuzz.trapmf(umur.universe, [0, 0, 5, 10])
umur['sedang'] = fuzz.trimf(umur.universe, [8, 18, 28])
umur['tua'] = fuzz.trapmf(umur.universe, [25, 30, 40, 40])

# =====================================
# MEMBERSHIP OUTPUT (HARGA, JUTA RUPIAH)
# Semesta 100-2000
# Murah 100-700 | Sedang 600-1400 | Mahal 1200-2000
# =====================================

harga['murah'] = fuzz.trapmf(harga.universe, [100, 100, 400, 700])
harga['sedang'] = fuzz.trimf(harga.universe, [600, 1000, 1400])
harga['mahal'] = fuzz.trapmf(harga.universe, [1200, 1600, 2000, 2000])
