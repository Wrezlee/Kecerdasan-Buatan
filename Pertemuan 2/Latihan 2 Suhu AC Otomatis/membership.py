import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# =====================================
# RANGE VARIABEL INPUT
# =====================================

suhu_ruangan = ctrl.Antecedent(np.arange(18, 41, 1), 'suhu_ruangan')
jumlah_orang = ctrl.Antecedent(np.arange(0, 21, 1), 'jumlah_orang')
kelembapan = ctrl.Antecedent(np.arange(20, 101, 1), 'kelembapan')

# =====================================
# RANGE VARIABEL OUTPUT
# =====================================

suhu_ac = ctrl.Consequent(np.arange(18, 29, 1), 'suhu_ac')

# =====================================
# MEMBERSHIP SUHU RUANGAN
# Semesta 18-40 C
# Dingin 18-24 | Normal 22-30 | Panas 28-40
# =====================================

suhu_ruangan['dingin'] = fuzz.trapmf(suhu_ruangan.universe, [18, 18, 20, 24])
suhu_ruangan['normal'] = fuzz.trimf(suhu_ruangan.universe, [22, 26, 30])
suhu_ruangan['panas'] = fuzz.trapmf(suhu_ruangan.universe, [28, 32, 40, 40])

# =====================================
# MEMBERSHIP JUMLAH ORANG
# Semesta 0-20 orang
# Sedikit 0-7 | Sedang 5-14 | Banyak 12-20
# =====================================

jumlah_orang['sedikit'] = fuzz.trapmf(jumlah_orang.universe, [0, 0, 3, 7])
jumlah_orang['sedang'] = fuzz.trimf(jumlah_orang.universe, [5, 9, 14])
jumlah_orang['banyak'] = fuzz.trapmf(jumlah_orang.universe, [12, 16, 20, 20])

# =====================================
# MEMBERSHIP KELEMBAPAN
# Semesta 20-100 %
# Rendah 20-45 | Sedang 40-70 | Tinggi 65-100
# =====================================

kelembapan['rendah'] = fuzz.trapmf(kelembapan.universe, [20, 20, 30, 45])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [40, 55, 70])
kelembapan['tinggi'] = fuzz.trapmf(kelembapan.universe, [65, 80, 100, 100])

# =====================================
# MEMBERSHIP OUTPUT (SUHU AC)
# Semesta 18-28 C
# Dingin 18-22 | Sedang 21-25 | Hangat 24-28
# =====================================

suhu_ac['dingin'] = fuzz.trapmf(suhu_ac.universe, [18, 18, 20, 22])
suhu_ac['sedang'] = fuzz.trimf(suhu_ac.universe, [21, 23, 25])
suhu_ac['hangat'] = fuzz.trapmf(suhu_ac.universe, [24, 26, 28, 28])
