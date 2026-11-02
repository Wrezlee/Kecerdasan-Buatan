import pandas as pd
import re
import string

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer

dokumen = [
    "malam minggu begini biasanya saudara aku nginep, terus kita craving either something to eat karena lapar maupun jajan, enaknya beli apa ya, please Kediri kota only kalau bisa ada delivery orderny",
    "Barusan lewat Monumen Memorial Park Kediri ada banner Gedhe bgt GRIB JAYA mau bikin acara disana, pdhl ini ormas lagi viral bgt gara-gara kericuhan demo 27 Agustus kemarin di JKT. Bisa-bisanya dapat ijin bikin acara di Kota Kediri",
    "hallo warga kediri, mau tanya dong, perbaikan jembatan habis alun” kediri keselatan arah ke tulungagung apa sudah selesai dan sudah bisa dilewati ya? terimakasih infonya"
]

stopword = StopWordRemoverFactory().create_stop_word_remover()
stemmer = StemmerFactory().create_stemmer()

def preprocessing(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    text = stopword.remove(' '.join(tokens))
    text = stemmer.stem(text)
    return text

dokumen_clean = [preprocessing(text) for text in dokumen]

print("HASIL PREPROCESSING")
for i, text in enumerate(dokumen_clean):
    print(f"Dokumen {i+1}: {text}")

tfidf = TfidfVectorizer()
X = tfidf.fit_transform(dokumen_clean)

feature_names = tfidf.get_feature_names_out()
scores = X.toarray()[0]

hasil = pd.DataFrame({
    "Kata": feature_names,
    "TF-IDF": scores
})

hasil = hasil.sort_values(by="TF-IDF", ascending=False)

print("DAFTAR KATA DENGAN TF-IDF TERTINGGI DOKUMEN :")
print(hasil.head(10).to_string(index=False))