from inference import DiagnosaPadi
from facts import Padi

# Membuat mesin inferensi
engine = DiagnosaPadi()
engine.reset()

# Memasukkan fakta/gejala
engine.declare(Padi(daun="menggulung"))
engine.declare(Padi(ulat="ada"))

#engine.declare(Padi(daun="menguning"))
#engine.declare(Padi(tanaman="kerdil"))

# Menjalankan inferensi
engine.run()

