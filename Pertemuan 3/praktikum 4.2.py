# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_excel("Dataset_nutrisi_makanan.xlsx", sheet_name="Dataset Asli")

print("=" * 60)
print("DATASET NUTRISI MAKANAN")
print("=" * 60)
print(df.head())
print("\nUkuran Data :", df.shape)

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================
X = df.iloc[:, 2:].copy()
print("Jumlah fitur :", X.shape[1])
print("\nFitur yang digunakan:")
print(X.columns.tolist())

X = X.replace("-", 0)
X = X.apply(pd.to_numeric, errors="coerce")
X = X.fillna(0)

print("\nMissing Value:")
print(X.isnull().sum().sum())

# ============================================================
# 3. NORMALISASI DATA
# ============================================================
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_norm = scaler.fit_transform(X)

print("Data setelah normalisasi:")
print(X_norm[:5])

# ============================================================
# 4. APPLY DBSCAN
# ============================================================
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.20, min_samples=5)
cluster = dbscan.fit_predict(X_norm)
df["Cluster"] = cluster

print("=" * 60)
print("HASIL DBSCAN")
print("=" * 60)
print(df[["Kode Baru", "Nama Bahan Makanan", "Cluster"]].head(20))

jumlah_cluster = len(set(cluster))
if -1 in cluster:
    jumlah_cluster -= 1

print("\nJumlah Cluster :", jumlah_cluster)

print("\nJumlah Data Tiap Cluster")
print(df["Cluster"].value_counts().sort_index())

noise = (cluster == -1).sum()
print("\nJumlah Noise :", noise)

# ============================================================
# 5. EVALUASI
# ============================================================
from sklearn.metrics import silhouette_score, davies_bouldin_score

mask = cluster != -1
X_eval = X_norm[mask]
cluster_eval = cluster[mask]

jumlah_cluster_eval = len(set(cluster_eval))

if jumlah_cluster_eval >= 2:
    ss = silhouette_score(X_eval, cluster_eval)
    dbi = davies_bouldin_score(X_eval, cluster_eval)

    print("=" * 60)
    print("HASIL EVALUASI")
    print("=" * 60)
    print("Jumlah Cluster :", jumlah_cluster_eval)
    print("Jumlah Noise :", noise)
    print("Silhouette Score :", round(ss, 4))
    print("Davies-Bouldin Index :", round(dbi, 4))
else:
    print("=" * 60)
    print("HASIL EVALUASI")
    print("=" * 60)
    print("Evaluasi tidak dapat dilakukan.")
    print("Minimal harus terdapat 2 cluster.")

df.to_excel("Hasil_DBSCAN_Makanan.xlsx", index=False)
print("\nHasil disimpan pada : Hasil_DBSCAN_Makanan.xlsx")

# ============================================================
# 7. VISUALISASI PCA
# ============================================================
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_norm)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster, cmap="tab20", s=40)
plt.title("DBSCAN Clustering Dataset Nutrisi Makanan")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(label="Cluster")
plt.grid(True)
plt.show()