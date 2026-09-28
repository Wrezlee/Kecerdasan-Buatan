from experta import Rule, MATCH
from facts import Mental

# Pemetaan kode gejala -> field pada Fact Mental (nilai "ya" / "tidak")
# G1  Sulit tidur                    -> tidur
# G2  Mudah cemas                    -> cemas
# G3  Sulit berkonsentrasi           -> konsentrasi
# G4  Merasa sedih berkepanjangan    -> sedih
# G5  Kehilangan minat beraktivitas  -> minat
# G6  Mudah lelah                    -> lelah
# G7  Merasa kewalahan               -> kewalahan
# G8  Jantung berdebar               -> jantung
# G9  Motivasi menurun               -> motivasi
# G10 Mudah panik                    -> panik


class MentalRules:

    # R1: IF G1 AND G3 AND G6 AND G7 THEN P1 (Kondisi mental relatif stabil) CF 0.85
    @Rule(
        Mental(tidur="ya", cf=MATCH.cf1),
        Mental(konsentrasi="ya", cf=MATCH.cf2),
        Mental(lelah="ya", cf=MATCH.cf3),
        Mental(kewalahan="ya", cf=MATCH.cf4)
    )
    def stabil(self, cf1, cf2, cf3, cf4):
        cf_rule = 0.85
        cf_evidence = min(cf1, cf2, cf3, cf4)
        cf = cf_evidence * cf_rule
        print("\nHasil : Kondisi mental relatif stabil")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R2: IF G1 AND G2 AND G6 AND G7 THEN P2 (Indikasi stres ringan) CF 0.95
    @Rule(
        Mental(tidur="ya", cf=MATCH.cf1),
        Mental(cemas="ya", cf=MATCH.cf2),
        Mental(lelah="ya", cf=MATCH.cf3),
        Mental(kewalahan="ya", cf=MATCH.cf4)
    )
    def stres_ringan(self, cf1, cf2, cf3, cf4):
        cf_rule = 0.95
        cf_evidence = min(cf1, cf2, cf3, cf4)
        cf = cf_evidence * cf_rule
        print("\nHasil : Indikasi stres ringan")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R3: IF G2 AND G8 AND G10 THEN P3 (Indikasi stres berat) CF 0.90
    @Rule(
        Mental(cemas="ya", cf=MATCH.cf1),
        Mental(jantung="ya", cf=MATCH.cf2),
        Mental(panik="ya", cf=MATCH.cf3)
    )
    def stres_berat(self, cf1, cf2, cf3):
        cf_rule = 0.90
        cf_evidence = min(cf1, cf2, cf3)
        cf = cf_evidence * cf_rule
        print("\nHasil : Indikasi stres berat")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R4: IF G4 AND G5 AND G9 THEN P4 (Indikasi gangguan kecemasan) CF 0.88
    @Rule(
        Mental(sedih="ya", cf=MATCH.cf1),
        Mental(minat="ya", cf=MATCH.cf2),
        Mental(motivasi="ya", cf=MATCH.cf3)
    )
    def gangguan_kecemasan(self, cf1, cf2, cf3):
        cf_rule = 0.88
        cf_evidence = min(cf1, cf2, cf3)
        cf = cf_evidence * cf_rule
        print("\nHasil : Indikasi gangguan kecemasan")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")

    # R5: IF G1=Tidak AND G2=Tidak AND G4=Tidak AND G5=Tidak AND G6=Tidak
    #     THEN P5 (Indikasi depresi ringan) CF 1.00
    # Catatan: rule ini dipicu ketika kelima gejala utama di atas
    # dinyatakan TIDAK muncul (nilai "tidak"), bukan ketika gejalanya ada.
    @Rule(
        Mental(tidur="tidak", cf=MATCH.cf1),
        Mental(cemas="tidak", cf=MATCH.cf2),
        Mental(sedih="tidak", cf=MATCH.cf3),
        Mental(minat="tidak", cf=MATCH.cf4),
        Mental(lelah="tidak", cf=MATCH.cf5)
    )
    def depresi_ringan(self, cf1, cf2, cf3, cf4, cf5):
        cf_rule = 1.00
        cf_evidence = min(cf1, cf2, cf3, cf4, cf5)
        cf = cf_evidence * cf_rule
        print("\nHasil : Indikasi depresi ringan")
        print(f"CF = {cf:.3f}")
        print(f"Tingkat Keyakinan = {cf*100:.2f}%")
