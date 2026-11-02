import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd

df = pd.read_excel("Dataset_Tekanan_Darah.xlsx")

print("=" * 50)
print("DATASET TEKANAN DARAH")
print("=" * 50)
print(df)

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================
X = df[["Usia", "Berat Badan (kg)"]]
y = df["Tekanan Darah"]

print("\nFitur:")
print(X)

print("\nTarget:")
print(y)

# ============================================================
# 3. APPLY DECISION TREE REGRESSOR
# ============================================================
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(
    criterion="squared_error",
    random_state=42
)
model.fit(X, y)

print("\nModel Decision Tree Regressor berhasil dibuat.")

# ============================================================
# VISUALISASI DECISION TREE
# ============================================================
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(16, 8))
plot_tree(
    model,
    feature_names=["Usia", "Berat Badan (kg)"],
    filled=True,
    rounded=True,
    precision=2
)
plt.title("Decision Tree Regressor - Prediksi Tekanan Darah")
plt.savefig("Decision_Tree_Tekanan_Darah.png", dpi=150, bbox_inches="tight")
plt.show()

# ============================================================
# 4. EVALUASI
# ============================================================
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

y_pred = model.predict(X)

mae = mean_absolute_error(y, y_pred)
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print("=" * 50)
print("HASIL EVALUASI")
print("=" * 50)
print("MAE :", round(mae, 4))
print("MSE :", round(mse, 4))
print("R2 :", round(r2, 4))

# ============================================================
# 5. SIMPAN MODEL
# ============================================================
import pickle

with open("model_tree.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel berhasil disimpan sebagai...")