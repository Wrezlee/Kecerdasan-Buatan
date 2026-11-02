import nltk
import re
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Download resource
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

text = "The service is VERY GOOD!!! The food is delicious and the price is CHEAP 😊"

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

stop_words = set(stopwords.words('english'))

tokens = [
    word for word in tokens
    if word not in stop_words
]

print("\nStopword Removal:")
print(tokens)

# ============================================================
# 5. STEMMING
# ============================================================

stemmer = PorterStemmer()

stemmed = [
    stemmer.stem(word)
    for word in tokens
]

print("\nStemming:")
print(stemmed)

# ============================================================
# 6. LEMMATIZATION
# ============================================================

lemmatizer = WordNetLemmatizer()

lemma = [
    lemmatizer.lemmatize(word)
    for word in tokens
]

print("\nLemmatization:")
print(lemma)