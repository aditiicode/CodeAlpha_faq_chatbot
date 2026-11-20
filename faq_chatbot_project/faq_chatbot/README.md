# Campus FAQ Chatbot

A simple FAQ chatbot built with Flask, NLTK, TF-IDF and cosine similarity, with a clean responsive chat UI.

## Requirements
- Python 3.9+
- pip

## Setup (Windows / VS Code)
1. Extract the project folder and open it in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate it (Windows):
   ```bash
   venv\\Scripts\\activate
   ```
5. Install libraries:
   ```bash
   pip install -r requirements.txt
   ```
6. Run:
   ```bash
   python app.py
   ```
   NLTK resources will download automatically the first time.
7. Open http://127.0.0.1:5000 in your browser.

## Customize FAQs
Edit `faqs.json`. Each item must have `question` and `answer` fields. Restart the app after edits.

## How it works
The FAQ questions are cleaned and lemmatized. TF-IDF converts them into numeric vectors. Incoming questions are vectorized and cosine similarity finds the closest FAQ. A minimum similarity threshold helps avoid unrelated matches.
