from skfuzzy import control as ctrl
from membership import kelembapan, suhu, penyiraman

# =====================================
# RULE
# =====================================

rules = [
    ctrl.Rule(kelembapan['kering'] & suhu['panas'], penyiraman['lama']),
    ctrl.Rule(kelembapan['kering'] & suhu['sedang'], penyiraman['lama']),
    ctrl.Rule(kelembapan['kering'] & suhu['dingin'], penyiraman['sedang']),
    ctrl.Rule(kelembapan['lembap'] & suhu['panas'], penyiraman['sedang']),
    ctrl.Rule(kelembapan['lembap'] & suhu['sedang'], penyiraman['sedang']),
    ctrl.Rule(kelembapan['lembap'] & suhu['dingin'], penyiraman['sebentar']),
    ctrl.Rule(kelembapan['basah'] & suhu['panas'], penyiraman['sebentar']),
    ctrl.Rule(kelembapan['basah'] & suhu['sedang'], penyiraman['sebentar']),
    ctrl.Rule(kelembapan['basah'] & suhu['dingin'], penyiraman['sebentar'])
]
