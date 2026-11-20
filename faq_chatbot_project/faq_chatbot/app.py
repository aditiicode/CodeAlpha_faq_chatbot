from flask import Flask, render_template, request, jsonify
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Download the NLTK resources required by this project on first run.
for resource, package in [("stopwords", "stopwords"), ("wordnet", "wordnet"), ("omw-1.4", "omw-1.4")]:
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(package, quiet=True)

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

with open("faqs.json", "r", encoding="utf-8") as file:
    FAQS = json.load(file)
def preprocess(text):
    """Lowercase, remove punctuation, tokenize, remove stopwords and lemmatize."""
    tokens = re.findall(r"[a-z]+", text.lower())
    cleaned = [LEMMATIZER.lemmatize(token) for token in tokens if token not in STOP_WORDS]
    return " ".join(cleaned)


# Each FAQ question is preprocessed and indexed when the server starts.
processed_questions = [preprocess(faq["question"]) for faq in FAQS]
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
faq_matrix = vectorizer.fit_transform(processed_questions)


def find_answer(user_question):
    cleaned_question = preprocess(user_question)
    if not cleaned_question.strip():
        return {"answer": "Please enter a question with a little more detail.", "similarity": 0.0, "matched_question": ""}

    user_vector = vectorizer.transform([cleaned_question])
    scores = cosine_similarity(user_vector, faq_matrix)[0]
    best_index = scores.argmax()
    best_score = float(scores[best_index])

    # Threshold prevents the chatbot from confidently answering unrelated questions.
    if best_score < 0.18:
        return {
            "answer": "Sorry, I couldn't find a close match in my FAQs. Try rephrasing or contact the college office.",
            "similarity": best_score,
            "matched_question": ""
        }

    return {
        "answer": FAQS[best_index]["answer"],
        "similarity": best_score,
        "matched_question": FAQS[best_index]["question"]
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please type a question.", "similarity": 0.0, "matched_question": ""}), 400
    result = find_answer(question)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
