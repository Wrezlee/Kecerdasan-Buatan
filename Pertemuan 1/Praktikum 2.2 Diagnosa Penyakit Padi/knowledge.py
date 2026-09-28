from experta import Rule
from facts import Padi


class PadiRules:

    @Rule(Padi(daun="menguning"),
          Padi(tanaman="kerdil"))
    def nitrogen(self):
        print("Diagnosa : Kekurangan Nitrogen")

    @Rule(Padi(daun="bercak_coklat"),
          Padi(ujung_daun="mengering"))
    def hawar(self):
        print("Diagnosa : Hawar Daun Bakteri")

    @Rule(Padi(daun="menggulung"),
          Padi(ulat="ada"))
    def ulat(self):
        print("Diagnosa : Serangan Ulat Daun")

    @Rule(Padi(daun="layu"),
          Padi(akar="busuk"))
    def akar(self):
        print("Diagnosa : Busuk Akar")

    @Rule(Padi(batang="busuk"),
          Padi(bulir="hampa"))
    def batang(self):
        print("Diagnosa : Busuk Batang")
