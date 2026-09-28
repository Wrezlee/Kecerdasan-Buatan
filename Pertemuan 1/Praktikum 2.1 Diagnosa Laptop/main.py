from inference import DiagnosaLaptop
from facts import Laptop

engine = DiagnosaLaptop()
engine.reset()

# Fakta yang diberikan pengguna
engine.declare(Laptop(power="hidup"))
engine.declare(Laptop(layar="hitam"))

#engine.declare(Laptop(lambat="ya"))
#engine.declare(Laptop(hdd="bunyi"))

# # Jalankan inferensi
engine.run()
