"""
Tool: Web Search using Serper.dev
Fetches top web results using the Serper.dev API.
"""

import requests
import os

def web_search(query, api_key=None):
    api_key = api_key or os.getenv("SERPER_API_KEY")
    if not api_key:
        return "[Web Search] API key not provided."

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key}
    payload = {"q": query}

    try:
        response = requests.post(url, headers=headers, json=payload)
        results = response.json().get("organic", [])
        return [
            {"title": r["title"], "link": r["link"], "snippet": r["snippet"]}
            for r in results[:3]
        ]
    except Exception as e:
        return f"[Web Search Error] {e}"
