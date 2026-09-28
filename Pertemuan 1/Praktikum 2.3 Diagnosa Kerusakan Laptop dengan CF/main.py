from inference import DiagnosaLaptop
from facts import Laptop

engine = DiagnosaLaptop()
engine.reset()

# ==========================
# Input Gejala + CF User
# ==========================
engine.declare(Laptop(power="mati", cf=0.8))
# Tingkat keyakinan user terhadap gejala power mati
engine.declare(Laptop(charger="hidup", cf=0.6))
# Tingkat keyakinan user terhadap gejala charger hidup

# engine.declare(Laptop(power="hidup", cf=0.8))
# engine.declare(Laptop(overheat="ya", cf=0.6))

# Jalankan inferensi
engine.run()

