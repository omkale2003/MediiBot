import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Keep numbers and words
    # Remove stopwords only for TF-IDF (not for keyword detection)
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text