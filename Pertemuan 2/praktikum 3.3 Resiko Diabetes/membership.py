import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# =====================================
# RANGE VARIABEL INPUT
# =====================================

gula = ctrl.Antecedent(np.arange(70, 251, 1), 'gula')
bmi = ctrl.Antecedent(np.arange(15, 41, 1), 'bmi')
umur = ctrl.Antecedent(np.arange(15, 81, 1), 'umur')

# =====================================
# RANGE VARIABEL OUTPUT
# =====================================

risiko = ctrl.Consequent(np.arange(0, 101, 1), 'risiko')

# =====================================
# MEMBERSHIP GULA DARAH
# =====================================

gula['normal'] = fuzz.trapmf(gula.universe, [70, 70, 90, 110])
gula['prediabetes'] = fuzz.trimf(gula.universe, [100, 140, 180])
gula['tinggi'] = fuzz.trapmf(gula.universe, [160, 180, 250, 250])

# =====================================
# MEMBERSHIP BMI
# =====================================

bmi['kurus'] = fuzz.trapmf(bmi.universe, [15, 15, 18, 20])
bmi['normal'] = fuzz.trimf(bmi.universe, [19, 23, 27])
bmi['gemuk'] = fuzz.trapmf(bmi.universe, [25, 30, 40, 40])

# =====================================
# MEMBERSHIP UMUR
# =====================================

umur['muda'] = fuzz.trapmf(umur.universe, [15, 15, 25, 35])
umur['dewasa'] = fuzz.trimf(umur.universe, [30, 45, 60])
umur['lansia'] = fuzz.trapmf(umur.universe, [55, 65, 80, 80])

# =====================================
# MEMBERSHIP OUTPUT
# =====================================

risiko['rendah'] = fuzz.trapmf(risiko.universe, [0, 0, 20, 40])
risiko['sedang'] = fuzz.trimf(risiko.universe, [30, 50, 70])
risiko['tinggi'] = fuzz.trapmf(risiko.universe, [60, 80, 100, 100])
