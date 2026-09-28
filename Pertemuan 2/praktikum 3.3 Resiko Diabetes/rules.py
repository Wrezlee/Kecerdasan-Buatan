from skfuzzy import control as ctrl
from membership import gula, bmi, umur, risiko

# =====================================
# RULE FUZZY
# =====================================

rules = [
    ctrl.Rule(gula['tinggi'] & bmi['gemuk'] & umur['lansia'], risiko['tinggi']),
    ctrl.Rule(gula['tinggi'] & bmi['gemuk'], risiko['tinggi']),
    ctrl.Rule(gula['prediabetes'] & bmi['gemuk'], risiko['sedang']),
    ctrl.Rule(gula['prediabetes'] & umur['dewasa'], risiko['sedang']),
    ctrl.Rule(gula['normal'] & bmi['normal'], risiko['rendah']),
    ctrl.Rule(gula['normal'] & bmi['kurus'], risiko['rendah']),
    ctrl.Rule(gula['tinggi'] & umur['muda'], risiko['sedang'])
]
