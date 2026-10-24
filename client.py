"""Semantic Deduplication Stream Filter Engine.
100% Python Standard Library.
"""

from typing import Dict, Any, List, Set, Tuple

class SemanticDeduplicationStreamFilter:
    """Filters near-duplicate content snippets in real time to avoid bloated context windows."""
    def __init__(self, jaccard_threshold: float = 0.65):
        self.threshold = jaccard_threshold
        self.seen_signatures: List[Tuple[str, Set[str]]] = []

    def _tokenize(self, text: str) -> Set[str]:
        cleaned = "".join(c.lower() if c.isalnum() else " " for c in text)
        return set(cleaned.split())

    def process_item(self, item_id: str, content: str) -> Dict[str, Any]:
        tokens = self._tokenize(content)
        if not tokens:
            return {"item_id": item_id, "action": "DROP_EMPTY", "similarity": 0.0}

        max_sim = 0.0
        matched_id = None
        for prev_id, prev_tokens in self.seen_signatures:
            intersection = len(tokens.intersection(prev_tokens))
            union = len(tokens.union(prev_tokens))
            sim = intersection / union if union > 0 else 0.0
            if sim > max_sim:
                max_sim = sim
                matched_id = prev_id

        if max_sim >= self.threshold:
            return {
                "item_id": item_id,
                "action": "DROPPED_DUPLICATE",
                "similarity": round(max_sim, 3),
                "duplicate_of": matched_id
            }
        else:
            self.seen_signatures.append((item_id, tokens))
            return {
                "item_id": item_id,
                "action": "ACCEPTED",
                "similarity": round(max_sim, 3)
            }
