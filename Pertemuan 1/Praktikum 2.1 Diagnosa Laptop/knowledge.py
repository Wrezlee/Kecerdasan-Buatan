from experta import Rule
from facts import Laptop

class LaptopRules:
    @Rule(Laptop (power="mati"),
          Laptop(Charger="mati"))
    def adaptor_rusak(self):
        print("Diagnosa : Adaptor rusak.")
        
    @Rule(Laptop(power="mati"),
          Laptop(charger="hidup"))
    def baterai(self):
        print("Diagnosa : Baterai atau Motherboar bermasalah.")
        
    @Rule(Laptop(power="hidup"),
          Laptop(layar="hitam"))
    def ram(self):
        print("Diagnosa : RAM longgar atau rusak.")
        
    @Rule(Laptop(power="hidup"),
          Laptop(overheat="ya"))
    def overheating(self):
        print("Diagnosa : Laptop mengalami overheating")
        
    @Rule(Laptop(lambat="ya"),
          Laptop(hdd="bunyi"))
    def harddisk(self):
        print("Diagnosa : Harddisk rusak.")