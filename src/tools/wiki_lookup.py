"""
Tool: Wikipedia Lookup
Fetches a short summary of a topic from Wikipedia.
"""

import wikipedia

def wiki_lookup(query: str, sentences=3):
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except Exception as e:
        return f"[Wikipedia Error] {e}"
