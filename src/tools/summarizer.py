"""
Tool: Summarizer
Uses transformers pipeline to summarize text
"""

from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def summarize_text(text, max_length=120):
    output = summarizer(text, max_length=max_length, do_sample=False)
    return output[0]['summary_text']
