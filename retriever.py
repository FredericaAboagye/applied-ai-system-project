import os
import re
from pathlib import Path
from typing import List


class LocalRetriever:
    def __init__(self, directory: str) -> None:
        self.directory = Path(directory)
        self.documents = self._load_documents()

    def _load_documents(self) -> List[str]:
        documents = []
        if not self.directory.exists():
            return documents

        for path in sorted(self.directory.glob("*.txt")):
            text = path.read_text(encoding="utf-8").strip()
            if text:
                documents.append(text)
        return documents

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        query_tokens = self._tokenize(query)
        scores = []

        for doc in self.documents:
            score = self._score_document(doc, query_tokens)
            scores.append((score, doc))

        scores.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scores[:top_k]]

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _score_document(self, doc: str, query_tokens: List[str]) -> int:
        tokens = self._tokenize(doc)
        return sum(tokens.count(token) for token in set(query_tokens))
