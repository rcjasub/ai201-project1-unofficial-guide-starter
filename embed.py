"""
Milestone 4a — Embed all chunks and store them in ChromaDB.

Run once (or re-run to rebuild the vector store):
    python embed.py

What this script does:
  1. Calls run_pipeline() from ingest.py to get the 74 chunks
  2. Loads the all-MiniLM-L6-v2 model (downloads ~90 MB on first run)
  3. Converts every chunk into a list of 384 numbers (its "embedding")
  4. Saves those numbers + the original text + metadata into ChromaDB
"""
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import run_pipeline

DB_PATH        = "chroma_db"       # folder where ChromaDB saves data to disk
COLLECTION     = "internship_guide"
EMBED_MODEL    = "all-MiniLM-L6-v2"


def build_vector_store() -> chromadb.Collection:
    # ── Step 1: get chunks from the ingestion pipeline ─────────────────────────
    chunks = run_pipeline()
    print()

    # ── Step 2: load the embedding model ───────────────────────────────────────
    print(f"Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    # ── Step 3: embed every chunk ───────────────────────────────────────────────
    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks…")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_list=True)

    # ── Step 4: set up ChromaDB and (re)create the collection ──────────────────
    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(COLLECTION)   # wipe old data on re-runs
    except Exception:
        pass
    collection = client.create_collection(
        COLLECTION,
        metadata={"hnsw:space": "cosine"},  # scores now range 0–1, matching milestone guidance
    )

    # ── Step 5: store embeddings + text + metadata ─────────────────────────────
    collection.add(
        ids        = [c["chunk_id"] for c in chunks],
        embeddings = embeddings,
        documents  = texts,
        metadatas  = [{"source": c["source"], "doc_type": c["doc_type"]} for c in chunks],
    )

    print(f"\nDone — {len(chunks)} chunks stored in {DB_PATH}/")
    return collection


if __name__ == "__main__":
    build_vector_store()
