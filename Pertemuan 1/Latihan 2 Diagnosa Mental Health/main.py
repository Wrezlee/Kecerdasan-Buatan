from inference import DiagnosaMental
from facts import Mental

engine = DiagnosaMental()
engine.reset()

# ==========================
# Input Gejala + CF User
# Contoh kasus: sulit tidur, mudah cemas, mudah lelah, merasa kewalahan
# -> mengarah ke Indikasi stres ringan
# ==========================
engine.declare(Mental(tidur="ya", cf=0.9))
engine.declare(Mental(cemas="ya", cf=0.8))
engine.declare(Mental(lelah="ya", cf=0.85))
engine.declare(Mental(kewalahan="ya", cf=0.7))

# Jalankan inferensi
engine.run()
