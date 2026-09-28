# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target

df = pd.DataFrame(X, columns=iris.feature_names)
df["Species"] = y

print("=" * 50)
print("DATASET IRIS")
print("=" * 50)
print(df.head())
print("\nUkuran Data :", df.shape)

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================
X = df[iris.feature_names]
y = df["Species"]

print("Fitur yang digunakan:")
print(X.columns.tolist())
print("\nJumlah Missing Value:")
print(X.isnull().sum())

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

dbscan = DBSCAN(eps=0.25, min_samples=5)
cluster = dbscan.fit_predict(X_norm)
df["Cluster"] = cluster

print("=" * 50)
print("HASIL DBSCAN")
print("=" * 50)
print(df.head(20))

jumlah_cluster = len(set(cluster))
if -1 in cluster:
    jumlah_cluster -= 1

jumlah_noise = list(cluster).count(-1)

# ============================================================
# 5. EVALUASI
# ============================================================
from sklearn.metrics import silhouette_score, davies_bouldin_score

mask = cluster != -1
X_eval = X_norm[mask]
cluster_eval = cluster[mask]

if len(set(cluster_eval)) > 1:
    silhouette = silhouette_score(X_eval, cluster_eval)
    dbi = davies_bouldin_score(X_eval, cluster_eval)

    print("=" * 50)
    print("HASIL EVALUASI")
    print("=" * 50)
    print("Jumlah Cluster :", jumlah_cluster)
    print("Jumlah Noise :", jumlah_noise)
    print("Silhouette Score :", round(silhouette, 4))
    print("Davies-Bouldin Index :", round(dbi, 4))
else:
    print("Evaluasi tidak dapat dilakukan.")
    print("Minimal harus terdapat 2 cluster.")

df.to_excel("Hasil_DBSCAN_Iris.xlsx", index=False)
print("\nHasil disimpan pada : Hasil_DBSCAN_Iris.xlsx")

# ============================================================
# 6. VISUALISASI
# ============================================================
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_norm)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster, cmap="tab10", s=70)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("DBSCAN Clustering - Iris")
plt.colorbar(label="Cluster")
plt.grid()

plt.show()