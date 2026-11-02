import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 1. READ DATA
# ============================================================
import kagglehub
import pandas as pd
from kagglehub import KaggleDatasetAdapter

file_path = "Salary_dataset.csv"
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "abhishek14398/salary-dataset-simple-linear-regression",
    file_path
)

print("=" * 50)
print("SALARY DATASET")
print("=" * 50)
print(df.head())
print("\nJumlah Data :", len(df))
print("\nNama Kolom :", df.columns.tolist())

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================
df = df.drop(columns=["Unnamed: 0"], errors="ignore")
df["YearsExperience"] = pd.to_numeric(df["YearsExperience"], errors="coerce")
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
df = df.dropna()

X = df[["YearsExperience"]]
y = df["Salary"]

print("\nData setelah preprocessing:")
print(df.head())

# ============================================================
# 3. APPLY DECISION TREE REGRESSOR
# ============================================================
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(
    criterion="squared_error",
    random_state=42
)
model.fit(X, y)

print("\nModel berhasil dibuat.")

# ============================================================
# VISUALISASI DECISION TREE
# ============================================================
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(18, 9))
plot_tree(
    model,
    feature_names=["YearsExperience"],
    filled=True,
    rounded=True,
    precision=2
)
plt.title("Decision Tree Regressor - Salary")
plt.savefig("Decision_Tree_Salary.png", dpi=150, bbox_inches="tight")
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
print("MAE :", round(mae, 2))
print("MSE :", round(mse, 2))
print("R2 :", round(r2, 4))

# ============================================================
# 5. SIMPAN MODEL
# ============================================================
import pickle

with open("model_tree.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel berhasil disimpan ...")