# Prediksi Penjualan Toyota (MLP) – UTS Kecerdasan Buatan

Jalankan lokal:
    pip install -r requirements.txt
    python app.py            # http://127.0.0.1:5000

Latih ulang model (opsional): `python train.py` (menghasilkan models/*.joblib dan report.json).
Dataset: data/toyota_wholesales.csv (GAIKINDO, wholesales Toyota Jan 2022 – Sep 2026); `build_dataset.py` mengekstrak dari PDF.

## Deploy (PythonAnywhere, gratis)
1. Daftar di pythonanywhere.com, tab Files: upload semua isi folder ini (atau zip lalu unzip lewat Bash console).
2. Bash console: `pip install --user flask scikit-learn pandas numpy joblib`
3. Tab Web > Add a new web app > Flask > Python 3.x (versi sama dengan console). Atur Source code ke folder proyek.
4. Edit file WSGI: `import sys; sys.path.insert(0,'/home/USERNAME/uts_toyota'); from app import app as application`
5. Reload. Alamat: USERNAME.pythonanywhere.com

## Deploy (Render)
New > Web Service > hubungkan repo GitHub berisi folder ini; Build: `pip install -r requirements.txt`; Start: `gunicorn app:app`.
