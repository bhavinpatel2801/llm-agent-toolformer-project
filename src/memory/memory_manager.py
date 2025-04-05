"""
Memory Manager using FAISS + Sentence Transformers
Stores and retrieves past summaries based on semantic similarity
"""
from pathlib import Path
import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class MemoryManager:
    def __init__(self, index_path=None):
        project_root = Path(__file__).resolve().parents[2]
        default_path = project_root / "data" / "memory_index.pkl"
        self.index_path = Path(index_path) if index_path else default_path

        self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
        self.index = faiss.IndexFlatL2(384)  # model outputs 384-dim vectors
        self.texts = []
        self.embeddings = []

        # ✅ Load if exists
        if self.index_path.exists():
            with open(self.index_path, "rb") as f:
                data = pickle.load(f)
                self.texts = data["texts"]
                self.embeddings = [e for e in data["embeddings"]]
                if self.embeddings:
                    embeddings_array = np.vstack(self.embeddings).astype("float32")
                    self.index.add(embeddings_array)

    def add_memory(self, text):
        if text in self.texts:
            return
        embedding = self.model.encode([text]).astype("float32")
        self.index.add(embedding)
        self.embeddings.append(embedding)
        self.texts.append(text)
        self._save()

    def search_memory(self, query, top_k=3):
        if not self.texts:
            return []

        query_vec = self.model.encode([query]).astype("float32")
        D, I = self.index.search(query_vec, top_k)
        similar_texts = []

        for dist, idx in zip(D[0], I[0]):
            if dist < 0.7:  # ✅ tuneable distance threshold
                similar_texts.append(self.texts[idx])

        return similar_texts

    def _save(self):
        os.makedirs(self.index_path.parent, exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump({
                "embeddings": self.embeddings,
                "texts": self.texts
            }, f)
