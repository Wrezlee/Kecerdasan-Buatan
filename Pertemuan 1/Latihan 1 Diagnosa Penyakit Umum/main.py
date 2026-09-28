from inference import DiagnosaPenyakit
from facts import Gejala

engine = DiagnosaPenyakit()
engine.reset()

# ==========================
# Input Gejala + CF User
# Contoh kasus: demam, batuk, pilek, sakit tenggorokan -> mengarah ke Influenza
# ==========================
engine.declare(Gejala(demam="ya", cf=0.9))
engine.declare(Gejala(batuk="ya", cf=0.8))
engine.declare(Gejala(pilek="ya", cf=0.7))
engine.declare(Gejala(tenggorokan="ya", cf=0.85))

# Jalankan inferensi
engine.run()
