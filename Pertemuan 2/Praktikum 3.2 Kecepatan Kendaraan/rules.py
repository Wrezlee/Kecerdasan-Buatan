from skfuzzy import control as ctrl
from membership import (
    jarak,
    lalu_lintas,
    jalan,
    kecepatan
)

rules = [
    ctrl.Rule(jarak['dekat'] & lalu_lintas['padat'] & jalan['buruk'], kecepatan['lambat']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['padat'] & jalan['sedang'], kecepatan['lambat']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['padat'] & jalan['baik'], kecepatan['sedang']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['sedang'] & jalan['buruk'], kecepatan['lambat']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['sedang'] & jalan['sedang'], kecepatan['sedang']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['sedang'] & jalan['baik'], kecepatan['sedang']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['sepi'] & jalan['buruk'], kecepatan['sedang']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['sepi'] & jalan['sedang'], kecepatan['sedang']),
    ctrl.Rule(jarak['dekat'] & lalu_lintas['sepi'] & jalan['baik'], kecepatan['sedang']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['padat'] & jalan['buruk'], kecepatan['lambat']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['padat'] & jalan['sedang'], kecepatan['sedang']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['padat'] & jalan['baik'], kecepatan['sedang']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['sedang'] & jalan['buruk'], kecepatan['sedang']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['sedang'] & jalan['sedang'], kecepatan['sedang']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['sedang'] & jalan['baik'], kecepatan['cepat']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['sepi'] & jalan['buruk'], kecepatan['sedang']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['sepi'] & jalan['sedang'], kecepatan['cepat']),
    ctrl.Rule(jarak['sedang'] & lalu_lintas['sepi'] & jalan['baik'], kecepatan['cepat']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['padat'] & jalan['buruk'], kecepatan['sedang']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['padat'] & jalan['sedang'], kecepatan['sedang']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['padat'] & jalan['baik'], kecepatan['cepat']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['sedang'] & jalan['buruk'], kecepatan['sedang']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['sedang'] & jalan['sedang'], kecepatan['cepat']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['sedang'] & jalan['baik'], kecepatan['cepat']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['sepi'] & jalan['buruk'], kecepatan['cepat']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['sepi'] & jalan['sedang'], kecepatan['cepat']),
    ctrl.Rule(jarak['jauh'] & lalu_lintas['sepi'] & jalan['baik'], kecepatan['cepat'])
]
