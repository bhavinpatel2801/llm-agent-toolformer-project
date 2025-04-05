"""
Research Agent:
Summarizes latest research on a given topic using arXiv + summarization tools.
"""

from tools.arxiv_search import fetch_arxiv_papers
from tools.summarizer import summarize_text

import json
import os
from datetime import datetime
from pathlib import Path


def save_results_to_json(results, query):
    # Get full path to this file
    current_file = Path(__file__).resolve()
    
    # Navigate to project root (../.. from agents/)
    project_root = current_file.parents[2]  # agents → src → project root
    
    # Create /data/ folder inside root
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    # Compose filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"research_{query.replace(' ', '_')}_{timestamp}.json"
    full_path = data_dir / filename

    # Write to JSON
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"[Agent] ✅ Results saved to: {full_path}")
    return str(full_path)


def run_research_agent(query: str, max_results: int = 3):
    print(f"[Agent] Starting research on: {query}")
    papers = fetch_arxiv_papers(query=query, max_results=max_results)
    
    summaries = []
    for i, paper in enumerate(papers):
        print(f"[Agent] Summarizing paper {i+1}: {paper['title']}")
        summary = summarize_text(paper['summary'])
        summaries.append({
            "title": paper['title'],
            "summary": summary,
            "url": paper['url']
        })

    save_results_to_json(summaries, query)
    return summaries


