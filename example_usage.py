from client import SemanticDeduplicationStreamFilter

filter_engine = SemanticDeduplicationStreamFilter(jaccard_threshold=0.6)
s1 = filter_engine.process_item("doc_1", "Quarterly retail sales forecast for Q4 increased 18 percent")
s2 = filter_engine.process_item("doc_2", "Quarterly retail sales forecast for Q4 grew by 18 percent")
s3 = filter_engine.process_item("doc_3", "Unrelated industrial robotics market penetration study in Asia")

print("=== Semantic Deduplication Telemetry ===")
print(f"Doc 1: {s1['action']}")
print(f"Doc 2: {s2['action']} (Similarity: {s2['similarity']}, Dupe of: {s2.get('duplicate_of')})")
print(f"Doc 3: {s3['action']}")
