import re
import string
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory
)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

text = "Pelayanannya BAGUS banget!!! Makanannya enak dan harganya MURAH 😊"

print("Teks Awal:")
print(text)

# ============================================================
# 1. CASE FOLDING
# ============================================================

text = text.lower()

print("\nCase Folding:")
print(text)

# ============================================================
# 2. CLEANING
# ============================================================

# Remove URL
text = re.sub(r'http\S+|www\S+', '', text)

# Remove Number
text = re.sub(r'\d+', '', text)

# Remove Punctuation
text = text.translate(
    str.maketrans('', '', string.punctuation)
)

# Remove Emoji
text = re.sub(
    r'[\U0001F300-\U0001F5FF'
    r'\U0001F600-\U0001F64F'
    r'\U0001F680-\U0001F6FF'
    r'\U0001F700-\U0001F77F'
    r'\U0001F780-\U0001F7FF'
    r'\U0001F800-\U0001F8FF'
    r'\U0001F900-\U0001F9FF'
    r'\U0001FA00-\U0001FAFF'
    r'\u2600-\u26FF'
    r'\u2700-\u27BF]+',
    '',
    text
)

print("\nCleaning:")
print(text)

# ============================================================
# 3. TOKENIZING
# ============================================================

tokens = word_tokenize(text)

print("\nTokenizing:")
print(tokens)

# ============================================================
# 4. STOPWORD REMOVAL
# ============================================================

factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()

text_stopword = stopword_remover.remove(' '.join(tokens))

tokens_stopword = text_stopword.split()

print("\nStopword Removal:")
print(tokens_stopword)

# ============================================================
# 5. STEMMING
# ============================================================

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

stemmed = [
    stemmer.stem(word)
    for word in tokens_stopword
]

print("\nStemming:")
print(stemmed)