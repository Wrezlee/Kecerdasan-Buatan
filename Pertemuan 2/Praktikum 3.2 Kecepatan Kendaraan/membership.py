import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# =====================================
# RANGE INPUT
# =====================================

jarak = ctrl.Antecedent(np.arange(0, 101, 1), 'jarak')
lalu_lintas = ctrl.Antecedent(np.arange(0, 101, 1), 'lalu_lintas')
jalan = ctrl.Antecedent(np.arange(0, 11, 1), 'jalan')

# =====================================
# RANGE OUTPUT
# =====================================

kecepatan = ctrl.Consequent(np.arange(0, 121, 1), 'kecepatan')

# =====================================
# MEMBERSHIP JARAK
# =====================================

jarak['dekat'] = fuzz.trimf(jarak.universe, [0, 0, 40])
jarak['sedang'] = fuzz.trimf(jarak.universe, [20, 50, 80])
jarak['jauh'] = fuzz.trimf(jarak.universe, [60, 100, 100])

# =====================================
# MEMBERSHIP LALU LINTAS
# =====================================

lalu_lintas['sepi'] = fuzz.trimf(lalu_lintas.universe, [0, 0, 40])
lalu_lintas['sedang'] = fuzz.trimf(lalu_lintas.universe, [20, 50, 80])
lalu_lintas['padat'] = fuzz.trimf(lalu_lintas.universe, [60, 100, 100])

# =====================================
# MEMBERSHIP KONDISI JALAN
# =====================================

jalan['buruk'] = fuzz.trimf(jalan.universe, [0, 0, 4])
jalan['sedang'] = fuzz.trimf(jalan.universe, [2, 5, 8])
jalan['baik'] = fuzz.trimf(jalan.universe, [6, 10, 10])

# =====================================
# MEMBERSHIP OUTPUT
# =====================================

kecepatan['lambat'] = fuzz.trimf(kecepatan.universe, [0, 20, 40])
kecepatan['sedang'] = fuzz.trimf(kecepatan.universe, [30, 60, 90])
kecepatan['cepat'] = fuzz.trimf(kecepatan.universe, [80, 120, 120])
