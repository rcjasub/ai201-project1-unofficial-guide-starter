"""
Milestone 4b — Query the vector store and return the top-k most relevant chunks.

Run to test retrieval against your 3 evaluation questions:
    python retrieve.py

What this script does:
  1. Converts your question into the same 384-number format as the chunks
  2. Asks ChromaDB: "which stored chunks have numbers closest to this question?"
  3. Returns the top-k chunks with their source file and a distance score

Distance score guide:
  < 0.3  — strong match, very relevant
  0.3–0.5 — decent match, probably useful
  > 0.6  — weak match, likely off-topic
"""
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH     = "chroma_db"
COLLECTION  = "internship_guide"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K       = 5

# Load model and collection once at import time so retrieve() is fast
_model      = SentenceTransformer(EMBED_MODEL)
_client     = chromadb.PersistentClient(path=DB_PATH)
_collection = _client.get_collection(COLLECTION)


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """
    Takes a plain-English question.
    Returns a list of the k most relevant chunks, each with:
      - text      : the chunk content
      - source    : which document it came from
      - distance  : how close the match is (lower = better)
    """
    query_embedding = _model.encode([query], convert_to_list=True)[0]

    results = _collection.query(
        query_embeddings = [query_embedding],
        n_results        = k,
        include          = ["documents", "metadatas", "distances"],
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "chunk_id": results["ids"][0][i],
            "text":     results["documents"][0][i],
            "source":   results["metadatas"][0][i]["source"],
            "doc_type": results["metadatas"][0][i]["doc_type"],
            "distance": round(results["distances"][0][i], 4),
        })
    return chunks


# ── Manual test against 3 evaluation questions ─────────────────────────────────

TEST_QUERIES = [
    "When should I start applying for summer SWE internships at Big Tech companies?",
    "What does Microsoft's software engineer intern interview process look like?",
    "How many LeetCode problems do I need to solve before I'm ready to interview?",
]


def print_results(query: str, results: list[dict]) -> None:
    print(f"\n{'═' * 64}")
    print(f"QUERY: {query}")
    print('═' * 64)
    for i, r in enumerate(results, 1):
        print(f"\n  [{i}] {r['source']}  |  distance: {r['distance']}")
        preview = r["text"][:350].replace("\n", " ")
        print(f"      {preview}{'…' if len(r['text']) > 350 else ''}")


if __name__ == "__main__":
    for q in TEST_QUERIES:
        print_results(q, retrieve(q))
