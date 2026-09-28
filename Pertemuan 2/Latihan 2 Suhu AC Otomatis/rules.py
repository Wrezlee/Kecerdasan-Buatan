from skfuzzy import control as ctrl
from membership import suhu_ruangan, jumlah_orang, kelembapan, suhu_ac

# =====================================
# RULE FUZZY
# =====================================

rules = [
    ctrl.Rule(suhu_ruangan['panas'] & jumlah_orang['banyak'] & kelembapan['tinggi'], suhu_ac['dingin']),   # 1
    ctrl.Rule(suhu_ruangan['panas'] & jumlah_orang['sedang'] & kelembapan['tinggi'], suhu_ac['dingin']),   # 2
    ctrl.Rule(suhu_ruangan['panas'] & jumlah_orang['sedikit'] & kelembapan['sedang'], suhu_ac['sedang']),  # 3
    ctrl.Rule(suhu_ruangan['normal'] & jumlah_orang['banyak'] & kelembapan['tinggi'], suhu_ac['sedang']),  # 4
    ctrl.Rule(suhu_ruangan['normal'] & jumlah_orang['sedang'] & kelembapan['sedang'], suhu_ac['sedang']),  # 5
    ctrl.Rule(suhu_ruangan['normal'] & jumlah_orang['sedikit'] & kelembapan['rendah'], suhu_ac['hangat']), # 6
    ctrl.Rule(suhu_ruangan['dingin'] & jumlah_orang['banyak'] & kelembapan['sedang'], suhu_ac['sedang']),  # 7
    ctrl.Rule(suhu_ruangan['dingin'] & jumlah_orang['sedang'] & kelembapan['rendah'], suhu_ac['hangat']),  # 8
    ctrl.Rule(suhu_ruangan['dingin'] & jumlah_orang['sedikit'] & kelembapan['rendah'], suhu_ac['hangat'])  # 9
]
