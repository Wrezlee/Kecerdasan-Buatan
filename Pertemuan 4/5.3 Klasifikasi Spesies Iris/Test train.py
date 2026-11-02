import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 1. READ DATA
# ============================================================
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["Species"] = iris.target

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

print("\nFitur X:")
print(X.head())

print("\nTarget y:")
print(y.head())

# ============================================================
# 3. APPLY DECISION TREE CLASSIFIER
# ============================================================
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    criterion="entropy",
    random_state=42
)
model.fit(X, y)

print("\nModel Decision Tree berhasil dibuat.")

# ============================================================
# VISUALISASI DECISION TREE
# ============================================================
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(18, 10))
plot_tree(
    model,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True,
    precision=2
)
plt.title("Decision Tree Classification - Iris")
plt.savefig("Decision_Tree_Iris.png", dpi=150, bbox_inches="tight")
plt.show()

# ============================================================
# 4. EVALUASI
# ============================================================
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

y_pred = model.predict(X)

accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred, average="weighted")
recall = recall_score(y, y_pred, average="weighted")
cm = confusion_matrix(y, y_pred)

print("=" * 50)
print("HASIL EVALUASI")
print("=" * 50)
print("Accuracy :", round(accuracy, 4))
print("Precision :", round(precision, 4))
print("Recall :", round(recall, 4))
print("\nConfusion Matrix:")
print(cm)

# ============================================================
# 5. SIMPAN MODEL TREE
# ============================================================
import pickle

model_data = {
    "model": model,
    "target_names": iris.target_names
}

with open("model_tree.pkl", "wb") as file:
    pickle.dump(model_data, file)

print("\nModel berhasil disimpan sebagai model_tree.pkl")