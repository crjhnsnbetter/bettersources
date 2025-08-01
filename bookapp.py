# bookapp.py
print("📚 Entered bookapp.py")

from waitress import serve
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from source_framer import frame_sources
from book_query_agent import search_books
print("🧠 Using book_query_agent alias")

load_dotenv()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    sources = None
    if request.method == "POST":
        topics = request.form.get("topics", "").split(",")
        goals = request.form.get("goals", "").split(",")
        book_results = search_books(topics, goals)
        sources = frame_sources(book_results, topics, goals)

    return render_template("index.html", sources=sources)

if __name__ == "__main__":
    try:
        print("🚀 Starting Flask server")
        serve(app, host="0.0.0.0", port=8080)
    except Exception as e:
        print(f"❌ App failed to start:\n{e}")
