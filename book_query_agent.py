# book_query_agent.py
# 🔍 Queries Open Library API based on topics and learning goals

import requests

def search_books(topics, goals):
    """
    Queries Open Library API using topics and learning goals.
    Returns a simplified list of book metadata for GPT framing.
    """
    base_url = "https://openlibrary.org/search.json"
    query = " ".join(topics + goals)
    print(f"📚 Open Library Query: {query}")

    params = {
        "q": query,
        "limit": 10
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return {"error": f"Open Library query failed: {response.status_code}"}

    results = response.json()
    books = results.get("docs", [])[:10]

    simplified = []
    for book in books:
        title = book.get("title")
        author = ", ".join(book.get("author_name", []))
        year = book.get("first_publish_year", "")
        key = book.get("key")
        link = f"https://openlibrary.org{key}" if key else None

        if title and link:
            simplified.append({
                "title": title,
                "author": author,
                "year": year,
                "link": link
            })

    return simplified
