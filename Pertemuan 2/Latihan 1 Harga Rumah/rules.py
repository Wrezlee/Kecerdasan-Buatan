from skfuzzy import control as ctrl
from membership import luas, lokasi, umur, harga

# =====================================
# RULE FUZZY
# =====================================

rules = [
    ctrl.Rule(luas['besar'] & lokasi['sangat'] & umur['baru'], harga['mahal']),        # 1
    ctrl.Rule(luas['besar'] & lokasi['strategis'] & umur['baru'], harga['mahal']),     # 2
    ctrl.Rule(luas['besar'] & lokasi['strategis'] & umur['sedang'], harga['mahal']),   # 3
    ctrl.Rule(luas['sedang'] & lokasi['sangat'] & umur['baru'], harga['mahal']),       # 4
    ctrl.Rule(luas['sedang'] & lokasi['strategis'] & umur['sedang'], harga['sedang']), # 5
    ctrl.Rule(luas['sedang'] & lokasi['kurang'] & umur['tua'], harga['murah']),        # 6
    ctrl.Rule(luas['kecil'] & lokasi['sangat'] & umur['baru'], harga['sedang']),       # 7
    ctrl.Rule(luas['kecil'] & lokasi['strategis'] & umur['sedang'], harga['murah']),   # 8
    ctrl.Rule(luas['kecil'] & lokasi['kurang'] & umur['tua'], harga['murah'])          # 9
]
