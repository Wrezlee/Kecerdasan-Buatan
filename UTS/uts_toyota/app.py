"""Aplikasi Flask: Prediksi Penjualan Mobil Toyota (MLP) - UTS Kecerdasan Buatan."""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE = Path(__file__).parent
app = Flask(__name__)

DF = pd.read_csv(BASE / "data" / "toyota_wholesales.csv")
REPORT = json.load(open(BASE / "models" / "report.json"))
ART = joblib.load(BASE / "models" / "mlp_toyota.joblib")
MODEL, SCALER, WINDOW = ART["model"], ART["scaler"], ART["window"]

NAMA_BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
              "Agustus", "September", "Oktober", "November", "Desember"]


def label(ym: str) -> str:
    y, m = ym.split("-")
    return f"{NAMA_BULAN[int(m) - 1]} {y}"


app.jinja_env.filters["bulan"] = label
app.jinja_env.filters["angka"] = lambda v, d=0: f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")

LAST = DF["bulan"].iloc[-1]


def months_between(a: str, b: str) -> int:
    ya, ma = map(int, a.split("-"))
    yb, mb = map(int, b.split("-"))
    return (yb - ya) * 12 + (mb - ma)


def add_month(ym: str, n: int) -> str:
    y, m = map(int, ym.split("-"))
    k = y * 12 + (m - 1) + n
    return f"{k // 12}-{k % 12 + 1:02d}"


def forecast(n_ahead: int):
    y = DF["penjualan"].values.astype(float)
    hist = list(SCALER.transform(y[-WINDOW:].reshape(-1, 1)).ravel())
    out = []
    for _ in range(n_ahead):
        p = float(MODEL.predict(np.array(hist[-WINDOW:]).reshape(1, -1))[0])
        out.append(p)
        hist.append(p)
    return SCALER.inverse_transform(np.array(out).reshape(-1, 1)).ravel()


def predict_month(ym: str):
    """Prediksi satu bulan. Untuk bulan yang sudah ada di data: nilai aktual + prediksi
    one-step-ahead dari 10 bulan sebelumnya. Untuk bulan masa depan: rekursif."""
    bulan = DF["bulan"].tolist()
    if ym in bulan:
        i = bulan.index(ym)
        if i < WINDOW:
            return None, "Data 10 bulan sebelumnya belum tersedia untuk bulan ini."
        x = SCALER.transform(DF["penjualan"].values[i - WINDOW:i].astype(float).reshape(-1, 1)).ravel()
        p = SCALER.inverse_transform([[MODEL.predict(x.reshape(1, -1))[0]]])[0][0]
        a = float(DF["penjualan"].iloc[i])
        return {"bulan": ym, "prediksi": float(p), "aktual": a, "jenis": "data historis"}, None
    n = months_between(LAST, ym)
    if n < 1 or n > 24:
        return None, f"Pilih bulan antara {label(DF['bulan'].iloc[WINDOW])} dan {label(add_month(LAST, 24))}."
    p = float(forecast(n)[-1])
    return {"bulan": ym, "prediksi": p, "aktual": None, "jenis": f"prakiraan {n} bulan ke depan"}, None


@app.route("/")
def index():
    stats = DF["penjualan"].describe()
    tahunan = DF.assign(tahun=DF.bulan.str[:4]).groupby("tahun")["penjualan"].agg(["sum", "count"]).reset_index()
    return render_template("index.html", df=DF, stats=stats, tahunan=tahunan.to_dict("records"), r=REPORT)


@app.route("/preprocessing")
def preprocessing():
    y = DF["penjualan"].values.astype(float)
    window_ex = [{"x": [int(v) for v in y[i:i + WINDOW]], "t": int(y[i + WINDOW]),
                  "target": label(DF.bulan.iloc[i + WINDOW])} for i in range(3)]
    return render_template("preprocessing.html", r=REPORT, ex=window_ex,
                           ymin=int(y[:-REPORT["test_n"]].min()), ymax=int(y[:-REPORT["test_n"]].max()),
                           missing=int(DF.penjualan.isna().sum()))


@app.route("/model")
def model_page():
    return render_template("model.html", r=REPORT, df=DF)


@app.route("/prediksi", methods=["GET", "POST"])
def prediksi():
    hasil = err = None
    pilihan = request.form.get("bulan", add_month(LAST, 1))
    if request.method == "POST":
        hasil, err = predict_month(pilihan)
    ahead = forecast(12)
    deret = [{"bulan": add_month(LAST, i + 1), "nilai": round(float(v))} for i, v in enumerate(ahead)]
    return render_template("prediksi.html", hasil=hasil, err=err, pilihan=pilihan, df=DF,
                           deret=deret, min_m=DF.bulan.iloc[WINDOW], max_m=add_month(LAST, 24), r=REPORT)


@app.route("/perbandingan")
def perbandingan():
    return render_template("perbandingan.html", r=REPORT)


@app.route("/api/predict")
def api_predict():
    ym = request.args.get("bulan", "")
    res, err = predict_month(ym)
    return (jsonify(error=err), 400) if err else jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
