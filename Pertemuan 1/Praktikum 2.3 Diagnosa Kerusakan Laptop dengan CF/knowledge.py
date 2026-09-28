from experta import Rule, MATCH
from facts import Laptop


class LaptopRules:

    # R1
    @Rule(
        Laptop(power="mati", cf=MATCH.cf_power),
        Laptop(charger="mati", cf=MATCH.cf_charger)
    )
    def adaptor(self, cf_power, cf_charger):
        cf_rule = 0.90
        cf_evidence = min(cf_power, cf_charger)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Adaptor Rusak")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R2
    @Rule(
        Laptop(power="mati", cf=MATCH.cf_power),
        Laptop(charger="hidup", cf=MATCH.cf_charger)
    )
    def baterai(self, cf_power, cf_charger):
        cf_rule = 0.85
        cf_evidence = min(cf_power, cf_charger)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Baterai atau Motherboard Bermasalah")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R3
    @Rule(
        Laptop(power="hidup", cf=MATCH.cf_power),
        Laptop(layar="hitam", cf=MATCH.cf_layar)
    )
    def ram(self, cf_power, cf_layar):
        cf_rule = 0.95
        cf_evidence = min(cf_power, cf_layar)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : RAM Longgar atau Rusak")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R4
    @Rule(
        Laptop(power="hidup", cf=MATCH.cf_power),
        Laptop(overheat="ya", cf=MATCH.cf_overheat)
    )
    def overheat(self, cf_power, cf_overheat):
        cf_rule = 0.80
        cf_evidence = min(cf_power, cf_overheat)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Overheating")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R5
    @Rule(
        Laptop(lambat="ya", cf=MATCH.cf_lambat),
        Laptop(hdd="bunyi", cf=MATCH.cf_hdd)
    )
    def harddisk(self, cf_lambat, cf_hdd):
        cf_rule = 0.90
        cf_evidence = min(cf_lambat, cf_hdd)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Harddisk Rusak")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")
