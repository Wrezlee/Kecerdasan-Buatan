# ============================================================
# TUGAS. PENGELOMPOKAN WILAYAH BERDASARKAN PRODUKSI TELUR DAN DAGING AYAM 2025
# Metode : Unsupervised Learning - DBSCAN
# Dataset: - Produksi Telur Ayam Petelur (Ton)
#          - Produksi Daging Ayam Ras Petelur (Ton)
#          - Produksi Daging Ayam Ras Pedaging (Ton)
# Preprocessing : Joining data (berdasarkan Provinsi)
# ============================================================

# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd
import glob

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def baca_produksi(pola_file, nama_kolom):
    """Membaca satu file produksi (Provinsi, Produksi 2025)."""
    file = glob.glob(pola_file)[0]
    data = pd.read_csv(file, encoding="utf-8-sig", header=None,
                       names=["Provinsi", nama_kolom])

    # Baris judul / tahun otomatis terbuang karena Provinsi atau nilainya kosong
    data[nama_kolom] = pd.to_numeric(data[nama_kolom], errors="coerce")
    data = data.dropna(subset=["Provinsi", nama_kolom])

    # Samakan penulisan nama provinsi agar join tidak gagal
    data["Provinsi"] = data["Provinsi"].astype(str).str.strip().str.upper()
    return data.reset_index(drop=True)


telur = baca_produksi("*Telur Ayam Petelur*.csv", "Telur_Ayam_Petelur")
petelur = baca_produksi("*Daging Ayam Ras Petelur*.csv", "Daging_Ayam_Petelur")
pedaging = baca_produksi("*Daging Ayam Ras Pedaging*.csv", "Daging_Ayam_Pedaging")

print("=" * 60)
print("DATASET PRODUKSI TELUR DAN DAGING AYAM 2025")
print("=" * 60)
print("Jumlah baris Telur Ayam Petelur   :", len(telur))
print("Jumlah baris Daging Ayam Petelur  :", len(petelur))
print("Jumlah baris Daging Ayam Pedaging :", len(pedaging))
print("\nContoh data Telur:")
print(telur.head())

# ============================================================
# 2. PREPROCESSING DATA : JOINING DATA
# ============================================================
# Gabungkan ketiga dataset berdasarkan kolom Provinsi
df = (telur
      .merge(petelur, on="Provinsi", how="inner")
      .merge(pedaging, on="Provinsi", how="inner"))

# Hapus baris total Indonesia (bukan provinsi)
df = df[df["Provinsi"] != "INDONESIA"]
df.reset_index(drop=True, inplace=True)

print("\nHasil join data:")
print(df.head())
print("\nJumlah provinsi setelah join :", len(df))

# Validasi: pastikan tidak ada provinsi yang hilang saat join
provinsi_hilang = set(telur["Provinsi"]) - set(df["Provinsi"]) - {"INDONESIA"}
if provinsi_hilang:
    print("[PERINGATAN] Provinsi tidak ter-join:", provinsi_hilang)

kolom_fitur = ["Telur_Ayam_Petelur", "Daging_Ayam_Petelur", "Daging_Ayam_Pedaging"]
X = df[kolom_fitur].copy()

print("\nJumlah fitur :", X.shape[1])
print("\nFitur yang digunakan:")
print(X.columns.tolist())
print("\nJumlah Missing Value:")
print(X.isnull().sum())

# Jika ada missing value, isi dengan 0
X = X.fillna(0)

print("\nStatistik Deskriptif (Ton):")
print(X.describe().round(2))

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

dbscan = DBSCAN(eps=0.07, min_samples=3)
cluster = dbscan.fit_predict(X_norm)
df["Cluster"] = cluster

print("=" * 60)
print("HASIL DBSCAN")
print("=" * 60)
print(df[["Provinsi", "Cluster"]])

jumlah_cluster = len(set(cluster))
if -1 in cluster:
    jumlah_cluster -= 1

print("\nJumlah Cluster :", jumlah_cluster)

print("\nJumlah Data Tiap Cluster (-1 = noise):")
print(df["Cluster"].value_counts().sort_index())

noise = (cluster == -1).sum()
print("\nJumlah Noise :", noise)

print("\nAnggota Tiap Cluster:")
for c in sorted(df["Cluster"].unique()):
    nama = "Noise" if c == -1 else f"Cluster {c}"
    print(f"- {nama}: {', '.join(df.loc[df['Cluster'] == c, 'Provinsi'])}")

# ============================================================
# 5. EVALUASI
# ============================================================
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Mengambil data yang bukan noise
mask = cluster != -1
X_eval = X_norm[mask]
cluster_eval = cluster[mask]

# Jumlah cluster setelah noise dikeluarkan
jumlah_cluster_eval = len(set(cluster_eval))

print("=" * 60)
print("HASIL EVALUASI")
print("=" * 60)

if jumlah_cluster_eval >= 2:
    # Silhouette Score
    ss = silhouette_score(X_eval, cluster_eval)
    # Davies-Bouldin Index
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
profil = df.groupby("Cluster").agg(
    Jumlah_Provinsi=("Provinsi", "count"),
    Rata_Telur=("Telur_Ayam_Petelur", "mean"),
    Rata_Daging_Petelur=("Daging_Ayam_Petelur", "mean"),
    Rata_Daging_Pedaging=("Daging_Ayam_Pedaging", "mean"),
).round(2)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)
print("=" * 60)
print("KARAKTERISTIK TIAP CLUSTER (rata-rata produksi, Ton)")
print("=" * 60)
print(profil)

# ============================================================
# 7. SIMPAN HASIL
# ============================================================
with pd.ExcelWriter("Hasil_DBSCAN_Produksi_Ayam.xlsx") as writer:
    df.to_excel(writer, sheet_name="Hasil Cluster", index=False)
    profil.reset_index().to_excel(writer, sheet_name="Profil Cluster", index=False)

print("\nHasil disimpan pada : Hasil_DBSCAN_Produksi_Ayam.xlsx")

# ============================================================
# 8. VISUALISASI PCA
# ============================================================
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_norm)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster, cmap="tab10", s=80,
            edgecolors="k", linewidths=0.4)

# Beri label provinsi yang menjadi noise agar mudah dibaca
for i, prov in enumerate(df["Provinsi"]):
    if cluster[i] == -1:
        plt.annotate(prov.title(), (X_pca[i, 0], X_pca[i, 1]),
                     fontsize=7, xytext=(4, 4), textcoords="offset points")

plt.margins(x=0.12, y=0.08)
plt.title("DBSCAN Clustering Produksi Telur dan Daging Ayam 2025")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(label="Cluster (-1 = noise)")
plt.grid(True)
plt.savefig("Tugas_Clustering.png", dpi=150, bbox_inches="tight")
plt.show()