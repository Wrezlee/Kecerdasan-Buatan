import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from newspaper import Article
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

# Download NLTK (jalankan sekali saja)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Input URL
url = input("Masukkan URL Berita : ")

# Mengambil berita
article = Article(url, language='id')
article.download()
article.parse()

judul = article.title
isi = article.text

print("\n" + "="*60)
print("JUDUL BERITA")
print("="*60)
print(judul)

print("\n" + "="*60)
print("ISI BERITA")
print("="*60)
print(isi[:1000])

# Preprocessing
text = isi.lower()
text = re.sub(r"http\S+|www\S+", "", text)  # Remove URL
text = re.sub(r"\d+", "", text)  # Remove Number
text = text.translate(str.maketrans('', '', string.punctuation))  # Remove Punctuation

tokens = word_tokenize(text)  # Tokenizing

stop_words = set(stopwords.words("indonesian"))
tokens = [word for word in tokens if word not in stop_words]  # Stopword Removal

stemmer = StemmerFactory().create_stemmer()
tokens = [stemmer.stem(word) for word in tokens]  # Stemming

clean_text = " ".join(tokens)

# TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([clean_text])

fitur = vectorizer.get_feature_names_out()
nilai = X.toarray()[0]

hasil = pd.DataFrame({
    "Kata": fitur,
    "TF-IDF": nilai
})

hasil = hasil.sort_values(by="TF-IDF", ascending=False)

# TOP KEYWORD
top5 = hasil.head(10)

print("\n" + "="*60)
print("TOP 5 KATA KUNCI")
print("="*60)
print(top5.to_string(index=False))

# Simpan ke Excel
hasil.to_excel("Hasil_TFIDF.xlsx", index=False)
print("\nHasil TF-IDF disimpan ke file Hasil_TFIDF.xlsx")

# Word Cloud
wordcloud = WordCloud(
    width=900,
    height=500,
    background_color="white"
).generate(clean_text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Word Cloud")
plt.show()

# Tampilkan Keyword
print("\n" + "="*60)
print("KATA KUNCI BERITA")
print("="*60)

for _, row in top5.iterrows():
    print(f"{row['Kata']} ({row['TF-IDF']:.4f})")