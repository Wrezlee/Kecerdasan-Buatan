import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ===========================================
# RANGE VARIABEL INPUT - OUTPUT
# ===========================================

kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
suhu = ctrl.Antecedent(np.arange(15, 41, 1), 'suhu')
penyiraman = ctrl.Consequent(np.arange(0, 31, 1), 'penyiraman')

# ===========================================
# FS MEMBERSHIP KELEMBAPAN
# ===========================================

kelembapan['kering'] = fuzz.trapmf(
    kelembapan.universe,
    [0, 0, 20, 40]
)

kelembapan['lembap'] = fuzz.trimf(
    kelembapan.universe,
    [30, 50, 70]
)

kelembapan['basah'] = fuzz.trapmf(
    kelembapan.universe,
    [60, 80, 100, 100]
)

# ===========================================
# FS MEMBERSHIP SUHU
# ===========================================

suhu['dingin'] = fuzz.trapmf(
    suhu.universe,
    [15, 15, 18, 24]
)

suhu['sedang'] = fuzz.trimf(
    suhu.universe,
    [22, 27, 32]
)

suhu['panas'] = fuzz.trapmf(
    suhu.universe,
    [30, 35, 40, 40]
)

# ===========================================
# OUTPUT PENYIRAMAN
# ===========================================

penyiraman['sebentar'] = fuzz.trapmf(
    penyiraman.universe,
    [0, 0, 5, 10]
)

penyiraman['sedang'] = fuzz.trimf(
    penyiraman.universe,
    [8, 15, 22]
)

penyiraman['lama'] = fuzz.trapmf(
    penyiraman.universe,
    [20, 25, 30, 30]
)