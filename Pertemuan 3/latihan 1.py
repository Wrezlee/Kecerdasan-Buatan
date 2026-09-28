# ============================================================
# LATIHAN 1. SEGMENTASI PELANGGAN (Mall Customer Segmentation)
# Metode : Unsupervised Learning - DBSCAN
# Dataset: Mall_Customers.csv (Kaggle: vjchoudhary7/customer-segmentation-tutorial-in-python)
# Pertanyaan: Bagaimana karakteristik kelompok pelanggan yang terbentuk?
# ============================================================

# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv("Mall_Customers.csv")

print("=" * 60)
print("DATASET MALL CUSTOMER")
print("=" * 60)
print(df.head())
print("\nUkuran Data :", df.shape)
print("\nStatistik Deskriptif:")
print(df.describe().round(2))

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================
# Fitur segmentasi : pendapatan tahunan & skor belanja
# (Age dan Gender tidak ikut clustering, dipakai untuk profiling)
fitur = ["Annual Income (k$)", "Spending Score (1-100)"]

X = df[fitur].copy()
X = X.apply(pd.to_numeric, errors="coerce")

print("\nJumlah fitur :", X.shape[1])
print("\nFitur yang digunakan:")
print(X.columns.tolist())
print("\nJumlah Missing Value:")
print(X.isnull().sum())

# Jika ada missing value, isi dengan median kolom
X = X.fillna(X.median())

# ============================================================
# 3. NORMALISASI DATA
# ============================================================
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_norm = scaler.fit_transform(X)

print("\nData setelah normalisasi:")
print(X_norm[:5])

# ============================================================
# 3B. (OPSIONAL) K-DISTANCE GRAPH UNTUK MEMILIH EPS
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

MIN_SAMPLES = 5
EPS = 0.09

nn = NearestNeighbors(n_neighbors=MIN_SAMPLES)
jarak, _ = nn.fit(X_norm).kneighbors(X_norm)
k_dist = np.sort(jarak[:, -1])

plt.figure(figsize=(8, 5))
plt.plot(k_dist)
plt.axhline(EPS, color="red", linestyle="--", label=f"eps = {EPS}")
plt.title(f"K-Distance Graph (k = {MIN_SAMPLES})")
plt.xlabel("Data (terurut)")
plt.ylabel(f"Jarak ke tetangga ke-{MIN_SAMPLES}")
plt.legend()
plt.grid(True)
plt.savefig("Latihan1_KDistance.png", dpi=150, bbox_inches="tight")
plt.show()

# ============================================================
# 4. APPLY DBSCAN
# ============================================================
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)
cluster = dbscan.fit_predict(X_norm)
df["Cluster"] = cluster

print("=" * 60)
print("HASIL DBSCAN")
print("=" * 60)
print(df.head(20))

jumlah_cluster = len(set(cluster))
if -1 in cluster:
    jumlah_cluster -= 1

noise = (cluster == -1).sum()

print("\nJumlah Cluster :", jumlah_cluster)
print("\nJumlah Data Tiap Cluster (-1 = noise):")
print(df["Cluster"].value_counts().sort_index())
print("\nJumlah Noise :", noise)

# ============================================================
# 5. EVALUASI
# ============================================================
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Data noise tidak diikutkan dalam evaluasi
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
# 6. KARAKTERISTIK TIAP CLUSTER (PROFILING)
# ============================================================
profil = df.groupby("Cluster").agg(
    Jumlah=("CustomerID", "count"),
    Rata_Umur=("Age", "mean"),
    Rata_Income=("Annual Income (k$)", "mean"),
    Min_Income=("Annual Income (k$)", "min"),
    Max_Income=("Annual Income (k$)", "max"),
    Rata_Spending=("Spending Score (1-100)", "mean"),
    Min_Spending=("Spending Score (1-100)", "min"),
    Max_Spending=("Spending Score (1-100)", "max"),
    Persen_Female=("Gender", lambda s: (s == "Female").mean() * 100),
).round(2)

# Pemberian label otomatis: dibandingkan dengan rata-rata keseluruhan
inc_mean, inc_std = df["Annual Income (k$)"].mean(), df["Annual Income (k$)"].std()
sp_mean, sp_std = df["Spending Score (1-100)"].mean(), df["Spending Score (1-100)"].std()


def tingkat(nilai, rata, std):
    if nilai > rata + 0.5 * std:
        return "Tinggi"
    if nilai < rata - 0.5 * std:
        return "Rendah"
    return "Sedang"


def beri_label(baris):
    if baris.name == -1:
        return "Noise / Outlier"
    inc = tingkat(baris["Rata_Income"], inc_mean, inc_std)
    sp = tingkat(baris["Rata_Spending"], sp_mean, sp_std)
    return f"Income {inc} - Spending {sp}"


profil["Karakteristik"] = profil.apply(beri_label, axis=1)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)
print("=" * 60)
print("KARAKTERISTIK TIAP CLUSTER")
print("=" * 60)
print(profil)

df["Karakteristik"] = df["Cluster"].map(profil["Karakteristik"])

# ============================================================
# 7. SIMPAN HASIL
# ============================================================
with pd.ExcelWriter("Hasil_DBSCAN_Mall_Customers.xlsx") as writer:
    df.to_excel(writer, sheet_name="Hasil Cluster", index=False)
    profil.reset_index().to_excel(writer, sheet_name="Profil Cluster", index=False)

print("\nHasil disimpan pada : Hasil_DBSCAN_Mall_Customers.xlsx")

# ============================================================
# 8. VISUALISASI
# ============================================================
# Karena hanya 2 fitur, scatter plot langsung memakai sumbu aslinya
plt.figure(figsize=(9, 6))
scatter = plt.scatter(
    df["Annual Income (k$)"],
    df["Spending Score (1-100)"],
    c=cluster,
    cmap="tab10",
    s=70,
    edgecolors="k",
    linewidths=0.4,
)
plt.title("DBSCAN Clustering - Segmentasi Pelanggan Mall")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.colorbar(scatter, label="Cluster (-1 = noise)")
plt.grid(True)
plt.savefig("Latihan1_Clustering.png", dpi=150, bbox_inches="tight")
plt.show()