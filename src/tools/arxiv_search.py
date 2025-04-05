"""
Tool: arXiv Search
Fetch latest papers on a given topic from arXiv
"""

import arxiv

def fetch_arxiv_papers(query: str, max_results: int = 3):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id
        })
    return results
