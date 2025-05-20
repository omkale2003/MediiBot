from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from .preprocessing import preprocess

def load_data(filepath):
    return pd.read_csv(filepath)

def train_tfidf(df, text_column):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df[text_column])
    return vectorizer, tfidf_matrix

def get_answer(user_query, vectorizer, tfidf_matrix, df):
    # First check for explicit intents using keywords
    lower_query = user_query.lower()
    
    # Intent 1: Greetings
    if any(greeting in lower_query for greeting in ["hi", "hello", "hii", "hey"]):
        return "Hello! How can I help you today?"
    
    # Intent 3: LCMV
    lcmv_keywords = ["lcmv", "lymphocytic choriomeningitis", "rodent", "urine", "droppings"]
    if any(keyword in lower_query for keyword in lcmv_keywords):
        return "LCMV infections occur through exposure to rodent excretions..."
    
    # If no intent matched, use TF-IDF fallback
    processed_query = preprocess(user_query)
    query_vector = vectorizer.transform([processed_query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # Add threshold to avoid bad matches
    if similarities.max() < 0.2:
        return "I'm not sure. Could you rephrase or ask about LCMV/malaria?"
    
    best_match_index = similarities.argmax()
    return df.iloc[best_match_index]['Answer']