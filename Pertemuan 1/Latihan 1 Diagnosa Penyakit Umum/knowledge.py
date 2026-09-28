from experta import Rule, MATCH
from facts import Gejala

# Pemetaan kode gejala -> field pada Fact Gejala
# G1  Demam               -> demam="ya"
# G2  Batuk                -> batuk="ya"
# G3  Pilek                -> pilek="ya"
# G4  Sakit tenggorokan     -> tenggorokan="ya"
# G5  Mual                 -> mual="ya"
# G6  Nyeri perut           -> perut="ya"
# G7  Diare                -> diare="ya"
# G8  Nyeri otot            -> otot="ya"
# G9  Sakit kepala          -> kepala="ya"
# G10 Nafsu makan menurun   -> nafsu_makan="turun"
# G11 Nyeri ulu hati        -> ulu_hati="ya"
# G12 Muntah                -> muntah="ya"

class PenyakitRules:

    # R1: IF G1 AND G2 AND G3 AND G4 THEN P1 (Influenza) CF 0.90
    @Rule(
        Gejala(demam="ya", cf=MATCH.cf1),
        Gejala(batuk="ya", cf=MATCH.cf2),
        Gejala(pilek="ya", cf=MATCH.cf3),
        Gejala(tenggorokan="ya", cf=MATCH.cf4)
    )
    def influenza(self, cf1, cf2, cf3, cf4):
        cf_rule = 0.90
        cf_evidence = min(cf1, cf2, cf3, cf4)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Influenza")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R2: IF G1 AND G5 AND G6 AND G7 THEN P2 (Tifus) CF 0.92
    @Rule(
        Gejala(demam="ya", cf=MATCH.cf1),
        Gejala(mual="ya", cf=MATCH.cf2),
        Gejala(perut="ya", cf=MATCH.cf3),
        Gejala(diare="ya", cf=MATCH.cf4)
    )
    def tifus(self, cf1, cf2, cf3, cf4):
        cf_rule = 0.92
        cf_evidence = min(cf1, cf2, cf3, cf4)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Tifus")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R3: IF G1 AND G8 AND G9 THEN P3 (DBD) CF 0.95
    @Rule(
        Gejala(demam="ya", cf=MATCH.cf1),
        Gejala(otot="ya", cf=MATCH.cf2),
        Gejala(kepala="ya", cf=MATCH.cf3)
    )
    def dbd(self, cf1, cf2, cf3):
        cf_rule = 0.95
        cf_evidence = min(cf1, cf2, cf3)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Demam Berdarah (DBD)")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R4: IF G5 AND G10 AND G11 THEN P4 (Gastritis) CF 0.88
    @Rule(
        Gejala(mual="ya", cf=MATCH.cf1),
        Gejala(nafsu_makan="turun", cf=MATCH.cf2),
        Gejala(ulu_hati="ya", cf=MATCH.cf3)
    )
    def gastritis(self, cf1, cf2, cf3):
        cf_rule = 0.88
        cf_evidence = min(cf1, cf2, cf3)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Gastritis (Maag)")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R5: IF G9 AND G11 THEN P5 (Migrain) CF 0.85
    @Rule(
        Gejala(kepala="ya", cf=MATCH.cf1),
        Gejala(ulu_hati="ya", cf=MATCH.cf2)
    )
    def migrain(self, cf1, cf2):
        cf_rule = 0.85
        cf_evidence = min(cf1, cf2)
        cf = cf_evidence * cf_rule
        print("\nDiagnosa : Migrain")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")
