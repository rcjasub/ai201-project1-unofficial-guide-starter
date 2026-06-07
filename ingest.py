"""
Milestone 3 — Document ingestion and chunking pipeline.

Run:  python ingest.py
Output: prints total chunk count and 5 sample chunks for inspection.
"""
import re
import random
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────
# 1 token ≈ 4 chars; sizes match planning.md Chunking Strategy

DOCS_DIR = Path("documents")

CHUNK_SIZES = {
    "review": 500,   # ~125 tokens — one Glassdoor anecdote per chunk
    "guide":  1400,  # ~350 tokens — one career-center section per chunk
    "qa":     None,  # split on Q+A boundaries, no fixed size
}
GUIDE_OVERLAP = 200  # ~50 tokens — protects facts that straddle section headers


# ── Document loading ────────────────────────────────────────────────────────────

def load_documents(docs_dir: Path) -> list[dict]:
    docs = []
    for path in sorted(docs_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if len(text) > 100:
            docs.append({"source": path.name, "text": text})
        else:
            print(f"SKIP  {path.name} — file is empty or a placeholder")
    return docs


# ── Cleaning ────────────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)           # HTML tags
    text = re.sub(r"&[a-z]+;|&#\d+;", " ", text)   # HTML entities (&amp; &#39;)
    text = re.sub(r"[ \t]{2,}", " ", text)          # repeated spaces/tabs
    text = re.sub(r"\n{3,}", "\n\n", text)          # excessive blank lines
    return text.strip()


# ── Doc-type detection ──────────────────────────────────────────────────────────

def get_doc_type(filename: str) -> str:
    if "glassdoor" in filename:
        return "review"
    if "qa" in filename or "resume" in filename or "interview_qa" in filename:
        return "qa"
    return "guide"


# ── Chunking strategies ─────────────────────────────────────────────────────────

def chunk_review(text: str, chunk_size: int) -> list[str]:
    """Split Glassdoor pages by paragraph, merging short header lines into the
    following content so metadata like 'I interviewed at X' doesn't become a
    standalone chunk."""
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks = []
    current = ""
    for p in paragraphs:
        if not current:
            current = p
        elif len(current) < 120 or len(current) + len(p) + 2 <= chunk_size:
            # merge short header lines or paragraphs that still fit
            current += "\n\n" + p
        else:
            if len(current) > 40:
                chunks.append(current)
            current = p
    if len(current) > 40:
        chunks.append(current)

    # Hard-split any chunk that still exceeds chunk_size
    result = []
    for chunk in chunks:
        if len(chunk) <= chunk_size:
            result.append(chunk)
        else:
            for i in range(0, len(chunk), chunk_size):
                piece = chunk[i : i + chunk_size].strip()
                if piece:
                    result.append(piece)
    return result


def chunk_qa(text: str) -> list[str]:
    """Split Q+A and markdown guides on section headers, then enforce a size cap
    so no single chunk balloons past 1,500 chars."""
    MAX_QA_CHUNK = 1500

    # Prefer markdown headers (## or ###); fall back to Q: / numbered patterns
    parts = re.split(r"\n(?=#{1,3}\s)", text)
    if len(parts) < 3:
        parts = re.split(
            r"\n(?=(?:Q:|[0-9]+\.\s|(?:How|What|When|Why|Should|Is|Are|Can)\s))",
            text,
        )

    chunks = []
    for part in parts:
        part = part.strip()
        if len(part) < 40:
            continue
        if len(part) <= MAX_QA_CHUNK:
            chunks.append(part)
        else:
            # Oversized section: slide through it with overlap
            for i in range(0, len(part), MAX_QA_CHUNK - 150):
                piece = part[i : i + MAX_QA_CHUNK].strip()
                if len(piece) > 40:
                    chunks.append(piece)

    if len(chunks) < 3:
        # Last resort: paragraph split
        chunks = [p.strip() for p in re.split(r"\n{2,}", text) if len(p.strip()) > 40]
    return chunks


def _snap_to_word(text: str, pos: int, search_back: bool = True) -> int:
    """Move pos to the nearest whitespace so chunks don't split mid-word."""
    if pos >= len(text):
        return len(text)
    if text[pos].isspace():
        return pos
    limit = max(0, pos - 60) if search_back else min(len(text), pos + 60)
    step = -1 if search_back else 1
    for i in range(pos, limit, step):
        if text[i].isspace():
            return i
    return pos


def chunk_guide(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Sliding-window split for career center guides with overlap.
    Snaps boundaries to whitespace so chunks never start or end mid-word."""
    chunks = []
    i = 0
    while i < len(text):
        end = _snap_to_word(text, min(i + chunk_size, len(text)), search_back=True)
        piece = text[i:end].strip()
        if len(piece) > 40:
            chunks.append(piece)
        next_i = _snap_to_word(text, i + chunk_size - overlap, search_back=False)
        i = next_i if next_i > i else i + 1
    return chunks


def chunk_document(text: str, doc_type: str) -> list[str]:
    if doc_type == "review":
        return chunk_review(text, CHUNK_SIZES["review"])
    if doc_type == "qa":
        return chunk_qa(text)
    return chunk_guide(text, CHUNK_SIZES["guide"], GUIDE_OVERLAP)


# ── Pipeline ────────────────────────────────────────────────────────────────────

def run_pipeline(docs_dir: Path = DOCS_DIR) -> list[dict]:
    docs = load_documents(docs_dir)
    print(f"\nLoaded {len(docs)} documents")

    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        doc_type = get_doc_type(doc["source"])
        chunks = chunk_document(cleaned, doc_type)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text":     chunk,
                "source":   doc["source"],
                "doc_type": doc_type,
                "chunk_id": f"{doc['source']}::chunk_{i:03d}",
            })

    print(f"Total chunks: {len(all_chunks)}")

    # ── Checkpoint: inspect 5 random chunks ────────────────────────────────────
    print("\n" + "─" * 60)
    print("5 SAMPLE CHUNKS (read each one — should be self-contained)")
    print("─" * 60)
    for sample in random.sample(all_chunks, min(5, len(all_chunks))):
        print(f"\n[{sample['chunk_id']}] type={sample['doc_type']}")
        print(sample["text"][:300] + ("…" if len(sample["text"]) > 300 else ""))
        print(f"Length: {len(sample['text'])} chars")

    return all_chunks


if __name__ == "__main__":
    run_pipeline()
