# source_framer.py

import os
from token_logger import log_token_usage
from legal_disclaimer import get_disclaimer_text
from dotenv import load_dotenv
import markdown

load_dotenv()
print("🧪 source_framer.py loaded")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def frame_sources(book_list, topics, goals):
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ["❌ No OpenAI API key found in environment.", get_disclaimer_text()]

    client = OpenAI(api_key=api_key)

    if not book_list or (isinstance(book_list, dict) and "error" in book_list):
        return ["No relevant book results found from Open Library.", get_disclaimer_text()]

    book_summary = "\n".join([
        f"- {b['title']} by {b['author']} ({b['year']}) — [Open Library Link]({b['link']})"
        for b in book_list
    ])

    prompt = (
        f"User is interested in the following topics: {', '.join(topics)}\n"
        f"Their learning goals are: {', '.join(goals)}\n\n"
        f"Here are 10 books retrieved from Open Library:\n{book_summary}\n\n"
        "Please suggest a few recommended starting points based on these books, using Markdown format. "
        "Summarize why they might be helpful for the user's goals, and embed the Open Library links inline."
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful research librarian. Based only on the provided book list and user goals, "
                "suggest the most relevant resources. Use inline Markdown links to Open Library. Keep it brief and helpful."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.5,
            max_tokens=700
        )
        reply = response.choices[0].message.content.strip()
        log_token_usage(response)
        reply_html = markdown.markdown(reply)
        return [reply_html, get_disclaimer_text()]
    except Exception as e:
        return [f"⚠️ GPT framing failed:\n\n{str(e)}", get_disclaimer_t]()
