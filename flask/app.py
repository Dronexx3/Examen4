from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Inicializar Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Descargar recursos necesarios
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Cargar y preprocesar datos
data = pd.read_csv('data.csv')
data.drop_duplicates(inplace=True)
data.reset_index(drop=True, inplace=True)
data.drop(columns=["isbn13", "isbn10", "subtitle", "thumbnail", "published_year", "average_rating", "num_pages", "ratings_count"], axis=1, inplace=True)
data['description'] = data['title'] + ' ' + data['authors'] + ' ' + data['categories'] + ' ' + data['description']

# Inicializar el preprocesamiento
en_stopwords = stopwords.words("english")
lemma = WordNetLemmatizer()

def clean(text):
    if isinstance(text, str):
        text = re.sub("[^A-Za-z1-9 ]", "", text)
        text = text.lower()
        tokens = word_tokenize(text)
        clean_list = [lemma.lemmatize(token) for token in tokens if token not in en_stopwords]
        return " ".join(clean_list)
    else:
        return ""

data['description'] = data['description'].apply(clean)

# Crear matriz TF-IDF
vectorizer = TfidfVectorizer()
test_matrix = vectorizer.fit_transform(data['description'])

def Recommendation_Cosine_similarity(matrix, keyword):
    idx_list = data[
        data['title'].str.contains(keyword, case=False, na=False) |
        data['description'].str.contains(keyword, case=False, na=False)
    ].index.tolist()
    
    if not idx_list:
        return "No books found with the given keyword."

    row_num = idx_list[0]
    similarity = cosine_similarity(matrix)
    similar_books = list(enumerate(similarity[row_num]))
    sorted_similar_books = sorted(similar_books, key=lambda x: x[1], reverse=True)[:6]
    
    recommendations = []
    for i, item in enumerate(sorted_similar_books):
        book_title = data.iloc[item[0]]["title"]
        recommendations.append({"rank": i + 1, "title": book_title, "score": item[1]})
    
    return recommendations

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Please provide a keyword parameter."}), 400

    recommendations = Recommendation_Cosine_similarity(test_matrix, keyword)
    if isinstance(recommendations, str):
        return jsonify({"message": recommendations}), 404

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



  




