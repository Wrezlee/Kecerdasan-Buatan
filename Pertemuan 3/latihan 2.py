# ============================================================
# LATIHAN 2. PENGELOMPOKAN WILAYAH
# Berdasarkan jumlah peserta didik jenjang SD, SMP, dan SMA (2024)
# Metode : Unsupervised Learning - DBSCAN
# Preprocessing : Binning data (equal-frequency / quantile)
# ============================================================

# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd
import numpy as np
import glob

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Nama file yang dicari untuk tiap jenjang (urut prioritas):
# 1) nama pendek yang disarankan, 2) nama panjang bawaan dataset
POLA_FILE = {
    "SD":  ["Siswa_SD.csv",  "*Sekolah Dasar (SD)*.csv"],
    "SMP": ["Siswa_SMP.csv", "*Sekolah Menengah Pertama (SMP)*.csv"],
    "SMA": ["Siswa_SMA.csv", "*Sekolah Menengah Atas (SMA)*.csv"],
}


def cari_kolom_murid(data, jenjang):
    """Mencari kolom jumlah murid total (Negeri+Swasta) pada satu jenjang."""
    j = jenjang.lower()
    kolom = [c for c in data.columns if "murid" in c.lower() and j in c.lower()]
    utama = [c for c in kolom if "negeri+swasta" in c.lower().replace(" ", "")]
    return (utama or kolom or [None])[0]


def baca_jenjang(jenjang):
    """Membaca jumlah murid (Negeri+Swasta) per provinsi untuk satu jenjang.
    Jika ada beberapa file cocok, dipakai file pertama yang berisi angka."""
    for pola in POLA_FILE[jenjang]:
        for file in sorted(glob.glob(pola)):
            data = pd.read_csv(file, encoding="utf-8-sig")
            kolom_murid = cari_kolom_murid(data, jenjang)
            if kolom_murid is None:
                continue

            data = data[[data.columns[0], kolom_murid]].copy()
            data.columns = ["Provinsi", f"Murid_{jenjang}"]

            # Nilai bukan angka (misal "...") menjadi NaN
            data[f"Murid_{jenjang}"] = pd.to_numeric(
                data[f"Murid_{jenjang}"].astype(str).str.replace(",", "", regex=False),
                errors="coerce")

            # Hapus baris keterangan / footer dan baris total Indonesia
            data["Provinsi"] = data["Provinsi"].astype(str).str.strip()
            data = data[data["Provinsi"].str.lower() != "indonesia"]
            data = data.dropna(subset=[f"Murid_{jenjang}"])

            if len(data) > 0:
                print(f"   [{jenjang}] file  : {file[:70]}")
                print(f"   [{jenjang}] kolom : {kolom_murid}")
                return data.reset_index(drop=True)
    return pd.DataFrame(columns=["Provinsi", f"Murid_{jenjang}"])


print("=" * 60)
print("MEMBACA DATASET PESERTA DIDIK")
print("=" * 60)

daftar = {}
for jenjang in ["SD", "SMP", "SMA"]:
    d = baca_jenjang(jenjang)
    if len(d) == 0:
        print(f"[PERINGATAN] Data {jenjang} kosong (semua nilai '...'), "
              f"jenjang {jenjang} DILEWATI.")
        print(f"             Unduh ulang dataset {jenjang} lalu jalankan kembali.")
    else:
        print(f"Data {jenjang}: {len(d)} provinsi")
        daftar[jenjang] = d

if len(daftar) < 2:
    raise SystemExit("Minimal 2 jenjang harus memiliki data untuk clustering.")

# Gabungkan semua jenjang berdasarkan Provinsi
df = None
for jenjang, d in daftar.items():
    df = d if df is None else df.merge(d, on="Provinsi", how="inner")

print("\nJenjang yang dipakai :", list(daftar.keys()))
print("Jumlah provinsi      :", len(df))
print(df.head())
print("\nStatistik Deskriptif:")
print(df.describe().round(0))

# ============================================================
# 2. PREPROCESSING DATA : BINNING
# ============================================================
# Binning equal-frequency (quantile) menjadi 5 kategori:
# 0 = Sangat Rendah ... 4 = Sangat Tinggi
JUMLAH_BIN = 5
NAMA_BIN = ["Sangat Rendah", "Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]

kolom_murid = [f"Murid_{j}" for j in daftar]
kolom_bin = [f"Bin_{j}" for j in daftar]

for kolom, kolom_b in zip(kolom_murid, kolom_bin):
    df[kolom_b] = pd.qcut(df[kolom], q=JUMLAH_BIN, labels=False, duplicates="drop")

X = df[kolom_bin].copy()
print("\nFitur hasil binning:")
print(X.columns.tolist())
print("\nJumlah Missing Value:")
print(X.isnull().sum().sum())
print("\nContoh hasil binning:")
print(df[["Provinsi"] + kolom_murid + kolom_bin].head(10))

# ============================================================
# 3. NORMALISASI DATA
# ============================================================
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_norm = scaler.fit_transform(X)

print("\nData setelah normalisasi:")
print(X_norm[:5])

# ============================================================
# 4. APPLY DBSCAN
# ============================================================
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Isi manual jika ingin parameter sendiri, contoh: EPS = 0.3 ; MIN_SAMPLES = 3
# Jika None, parameter dipilih otomatis lewat grid search (silhouette terbaik)
EPS = None
MIN_SAMPLES = None
MAKS_NOISE = 0.25   # batas maksimal proporsi noise pada grid search


def evaluasi(label):
    mask = label != -1
    k = len(set(label[mask]))
    if k >= 2:
        return (k, (~mask).sum(),
                silhouette_score(X_norm[mask], label[mask]),
                davies_bouldin_score(X_norm[mask], label[mask]))
    return (k, (~mask).sum(), None, None)


if EPS is None or MIN_SAMPLES is None:
    hasil_grid = []
    for eps in np.round(np.arange(0.10, 0.61, 0.05), 2):
        for ms in range(3, 7):
            label = DBSCAN(eps=eps, min_samples=ms).fit_predict(X_norm)
            k, n_noise, ss, dbi = evaluasi(label)
            if ss is not None and n_noise <= MAKS_NOISE * len(df):
                hasil_grid.append((eps, ms, k, n_noise, ss, dbi))

    grid = pd.DataFrame(hasil_grid, columns=["eps", "min_samples", "cluster",
                                             "noise", "silhouette", "dbi"])
    if grid.empty:
        raise SystemExit("Tidak ada parameter yang menghasilkan >= 2 cluster.")

    grid = grid.round({"silhouette": 4, "dbi": 4})
    grid = grid.sort_values(["silhouette", "dbi", "noise"],
                            ascending=[False, True, True]).reset_index(drop=True)
    print("=" * 60)
    print("GRID SEARCH PARAMETER DBSCAN (10 terbaik)")
    print("=" * 60)
    print(grid.head(10))

    EPS = float(grid.loc[0, "eps"])
    MIN_SAMPLES = int(grid.loc[0, "min_samples"])

print("\nParameter terpilih : eps =", EPS, "| min_samples =", MIN_SAMPLES)

dbscan = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)
cluster = dbscan.fit_predict(X_norm)
df["Cluster"] = cluster

print("=" * 60)
print("HASIL DBSCAN")
print("=" * 60)
print(df[["Provinsi"] + kolom_murid + ["Cluster"]])

jumlah_cluster = len(set(cluster))
if -1 in cluster:
    jumlah_cluster -= 1

noise = (cluster == -1).sum()

print("\nJumlah Cluster :", jumlah_cluster)
print("\nJumlah Data Tiap Cluster (-1 = noise):")
print(df["Cluster"].value_counts().sort_index())
print("\nJumlah Noise :", noise)

print("\nAnggota Tiap Cluster:")
for c in sorted(df["Cluster"].unique()):
    nama = "Noise" if c == -1 else f"Cluster {c}"
    print(f"- {nama}: {', '.join(df.loc[df['Cluster'] == c, 'Provinsi'])}")

# ============================================================
# 5. EVALUASI
# ============================================================
mask = cluster != -1
X_eval = X_norm[mask]
cluster_eval = cluster[mask]

jumlah_cluster_eval = len(set(cluster_eval))

print("=" * 60)
print("HASIL EVALUASI")
print("=" * 60)

if jumlah_cluster_eval >= 2:
    ss = silhouette_score(X_eval, cluster_eval)
    dbi = davies_bouldin_score(X_eval, cluster_eval)

    print("Jumlah Cluster :", jumlah_cluster_eval)
    print("Jumlah Noise :", noise)
    print("Silhouette Score :", round(ss, 4))
    print("Davies-Bouldin Index :", round(dbi, 4))
else:
    print("Evaluasi tidak dapat dilakukan.")
    print("Minimal harus terdapat 2 cluster.")

# ============================================================
# 6. KARAKTERISTIK TIAP CLUSTER
# ============================================================
agregasi = {"Provinsi": "count"}
for kolom, kolom_b in zip(kolom_murid, kolom_bin):
    agregasi[kolom] = "mean"
    agregasi[kolom_b] = "mean"

profil = df.groupby("Cluster").agg(agregasi).rename(columns={"Provinsi": "Jumlah_Provinsi"})
profil = profil.round(2)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)
print("=" * 60)
print("KARAKTERISTIK TIAP CLUSTER (rata-rata)")
print("=" * 60)
print(profil)

# ============================================================
# 7. SIMPAN HASIL
# ============================================================
with pd.ExcelWriter("Hasil_DBSCAN_Peserta_Didik.xlsx") as writer:
    df.to_excel(writer, sheet_name="Hasil Cluster", index=False)
    profil.reset_index().to_excel(writer, sheet_name="Profil Cluster", index=False)

print("\nHasil disimpan pada : Hasil_DBSCAN_Peserta_Didik.xlsx")

# ============================================================
# 8. VISUALISASI PCA
# ============================================================
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_norm)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster, cmap="tab10", s=110, alpha=0.7,
            edgecolors="k")
plt.title("DBSCAN Clustering Wilayah Berdasarkan Jumlah Peserta Didik")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(label="Cluster (-1 = noise)")
plt.grid(True)
plt.savefig("Latihan2_Clustering.png", dpi=150, bbox_inches="tight")
plt.show()