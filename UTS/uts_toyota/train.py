"""Latih MLP untuk prediksi penjualan Toyota (GAIKINDO wholesales bulanan).
Mengikuti metodologi jurnal: window 10 bulan -> 1 output, hidden layer 10..15
neuron, ReLU, Adam, 300 epoch, 6 bulan terakhir sebagai data uji."""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

BASE = Path(__file__).parent
WINDOW, TEST_N, EPOCHS = 10, 6, 300
HIDDEN = [10, 11, 12, 13, 14, 15]
SEEDS = list(range(10))

df = pd.read_csv(BASE / "data" / "toyota_wholesales.csv")
y = df["penjualan"].values.astype(float)

# Scaler hanya difit pada data latih (6 bulan terakhir tidak dilihat) -> tanpa kebocoran
n_train_pts = len(y) - TEST_N
scaler = MinMaxScaler().fit(y[:n_train_pts].reshape(-1, 1))
ys = scaler.transform(y.reshape(-1, 1)).ravel()


def make_xy(series):
    X = np.array([series[i:i + WINDOW] for i in range(len(series) - WINDOW)])
    t = series[WINDOW:]
    return X, t


X, t = make_xy(ys)
n_samples = len(t)
X_tr, t_tr = X[:n_samples - TEST_N], t[:n_samples - TEST_N]
X_te, t_te = X[n_samples - TEST_N:], t[n_samples - TEST_N:]
actual_te = y[-TEST_N:]
months_te = df["bulan"].values[-TEST_N:].tolist()


def inv(a):
    return scaler.inverse_transform(np.asarray(a).reshape(-1, 1)).ravel()


def metrics(a, p):
    e = a - p
    return {
        "mae": float(np.mean(np.abs(e))),
        "mse": float(np.mean(e ** 2)),
        "rmse": float(np.sqrt(np.mean(e ** 2))),
        "mape": float(np.mean(np.abs(e / a)) * 100),
    }


def fit(h, seed):
    m = MLPRegressor(hidden_layer_sizes=(h,), activation="relu", solver="adam",
                     max_iter=EPOCHS, random_state=seed, learning_rate_init=0.01,
                     tol=0, n_iter_no_change=EPOCHS + 1)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # ConvergenceWarning pada 300 epoch
        m.fit(X_tr, t_tr)
    return m


results, best = [], None
for h in HIDDEN:
    runs = []
    for s in SEEDS:
        m = fit(h, s)
        pred = inv(m.predict(X_te))
        met = metrics(actual_te, pred)
        met_tr = metrics(inv(t_tr), inv(m.predict(X_tr)))
        runs.append((met, met_tr, pred, m, s))
    # seed utama = 42-ekuivalen: seed 0 (dilaporkan sebagai hasil arsitektur)
    main = runs[0]
    mean_mae = float(np.mean([r[0]["mae"] for r in runs]))
    mean_mse = float(np.mean([r[0]["mse"] for r in runs]))
    results.append({
        "arsitektur": f"10-{h}-1", "hidden": h,
        **{k: round(v, 4) for k, v in main[0].items()},
        "train_mae": round(main[1]["mae"], 4),
        "mean_mae_10seed": round(mean_mae, 4),
        "mean_mse_10seed": round(mean_mse, 4),
        "pred_test": [round(float(v), 2) for v in main[2]],
    })
    if best is None or main[0]["mae"] < best[0]["mae"]:
        best = (main[0], h, main[3], main[2], main[4])
    print(f"10-{h}-1  MAE={main[0]['mae']:.2f} MSE={main[0]['mse']:.0f} "
          f"MAPE={main[0]['mape']:.2f}%  | rata2 10 seed MAE={mean_mae:.2f}")

met, h, model, pred_te, seed = best
print(f"\nTerbaik: 10-{h}-1 (seed {seed}) MAE={met['mae']:.2f} MSE={met['mse']:.0f} MAPE={met['mape']:.2f}%")

# Pembanding: baseline naif (nilai bulan sebelumnya)
naive = y[-TEST_N - 1:-1]
baseline = metrics(actual_te, naive)
print("Baseline naif:", {k: round(v, 2) for k, v in baseline.items()})

# Jurnal (Tabel 11, arsitektur 10-15-1) -> hitung ulang MSE
j_act = np.array([28128, 28970, 27336, 29471, 21518, 28178], float)
j_prd = np.array([27843.523438, 28014.414062, 29699.933594, 26818.810547,
                  20714.095703, 23962.378906])
jm = metrics(j_act, j_prd)
print("Jurnal (dihitung ulang):", {k: round(v, 4) for k, v in jm.items()})

# Prediksi ke depan secara rekursif (sampai Des 2026 dst.)
def forecast(n_ahead):
    hist = list(ys[-WINDOW:])
    out = []
    for _ in range(n_ahead):
        p = float(model.predict(np.array(hist[-WINDOW:]).reshape(1, -1))[0])
        out.append(p)
        hist.append(p)
    return inv(out)

# Simpan artefak
(BASE / "models").mkdir(exist_ok=True)
joblib.dump({"model": model, "scaler": scaler, "window": WINDOW}, BASE / "models" / "mlp_toyota.joblib")

# prediksi in-sample/test untuk grafik
all_pred = inv(model.predict(X))
months_all = df["bulan"].values[WINDOW:].tolist()
report = {
    "n_data": len(y), "periode": [df.bulan.iloc[0], df.bulan.iloc[-1]],
    "window": WINDOW, "epochs": EPOCHS, "test_n": TEST_N,
    "n_train_samples": int(len(t_tr)), "n_test_samples": int(len(t_te)),
    "best": {"arsitektur": f"10-{h}-1", "seed": seed, **{k: round(v, 4) for k, v in met.items()}},
    "baseline_naif": {k: round(v, 4) for k, v in baseline.items()},
    "jurnal": {"arsitektur": "10-15-1", **{k: round(v, 4) for k, v in jm.items()},
               "bulan": ["2022-12", "2023-01", "2023-02", "2023-03", "2023-04", "2023-05"],
               "aktual": j_act.tolist(), "prediksi": [round(v, 2) for v in j_prd]},
    "results": results,
    "test": {"bulan": months_te, "aktual": actual_te.tolist(),
             "prediksi": [round(float(v), 2) for v in pred_te]},
    "fit_all": {"bulan": months_all, "prediksi": [round(float(v), 2) for v in all_pred]},
}
with open(BASE / "models" / "report.json", "w") as f:
    json.dump(report, f, indent=1)
print("\nTersimpan di models/")
print("Prakiraan 3 bulan ke depan:", [round(float(v)) for v in forecast(3)])
