from inference import DiagnosaPadi
from facts import Padi

engine = DiagnosaPadi()
engine.reset()

# ==========================
# Input Gejala + CF User
# ==========================
engine.declare(Padi(daun="menggulung", cf=1.0))
engine.declare(Padi(ulat="ada", cf=0.8))

# engine.declare(Padi(daun="bercak_coklat", cf=1.0))
# engine.declare(Padi(ujung_daun="mengering", cf=0.8))

# Jalankan inferensi
engine.run()
