from text import question_dict

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity




def preprocess_text(text):
    text = text.lower()  
    tokens = word_tokenize(text)  
    return ' '.join(tokens) 


def build_tfidf_matrix(texts):
    tfidf_vectorizer = TfidfVectorizer(preprocessor=preprocess_text)
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    return tfidf_matrix.toarray()  


def find_closest_answer(question):
    processed_question = preprocess_text(question)
    question_dict_keys = list(question_dict.keys())  
    tfidf_matrix = build_tfidf_matrix(question_dict_keys + [processed_question])
    question_vector = tfidf_matrix[-1]  
    similarities = cosine_similarity([question_vector], tfidf_matrix[:-1])  
    closest_index = similarities.argmax()  
    closest_answer = list(question_dict.values())[closest_index]  
    return closest_answer


