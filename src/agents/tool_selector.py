from tools.wiki_lookup import wiki_lookup
from tools.web_search import web_search
from tools.pdf_reader import extract_pdf_text
from tools.summarizer import summarize_text
import os

def tool_selector(query, context_type="text", file_path=None, api_keys={}):
    """
    context_type: 'wiki', 'web', 'pdf'
    file_path: optional path for PDF context
    api_keys: {'SERPER_API_KEY': '...'}
    """

    if context_type == "wiki":
        summary = wiki_lookup(query)
        return {"source": "Wikipedia", "result": summary}

    elif context_type == "web":
        results = web_search(query, api_key=api_keys.get("SERPER_API_KEY"))
        return {"source": "Web Search", "result": results}

    elif context_type == "pdf" and file_path:
        text = extract_pdf_text(file_path)
        summary = summarize_text(text[:1000])  # summarize first chunk
        return {"source": "PDF File", "result": summary}

    else:
        return {"source": "None", "result": "[Tool Selector] Invalid context type or missing input."}
