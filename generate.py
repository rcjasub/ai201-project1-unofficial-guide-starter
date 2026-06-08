"""
Milestone 5a — Grounded generation using Groq.

Takes a question, retrieves the top-k chunks, and asks the LLM to answer
using ONLY those chunks. Source attribution is both instructed (in the system
prompt) and guaranteed programmatically (appended after the LLM response).

Usage:
    python generate.py
"""
import os
from groq import Groq
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL   = "llama-3.3-70b-versatile"

# ── Grounding system prompt ────────────────────────────────────────────────────
# "Only" and "must not" are load-bearing words here — vague instructions like
# "try to use the documents" leave the model room to fill gaps with training data.

SYSTEM_PROMPT = """\
You are an unofficial guide assistant helping college students navigate tech internship recruiting.

You must answer the user's question using ONLY the information in the documents provided below.
Do not use any outside knowledge or training data — even if you know the answer from elsewhere.
If the provided documents do not contain enough information to answer the question, respond with exactly:
"I don't have enough information in my documents to answer that."

When you answer, cite which document(s) your answer came from by referencing the source label
(e.g. "According to doc_01_cornell_guide.txt, ..."). Be specific and concise.\
"""


def ask(question: str, k: int = 5) -> dict:
    """
    Full RAG pipeline for one question.

    Returns:
        answer  — the LLM's grounded response
        sources — deduplicated list of source filenames (programmatic, always present)
        chunks  — the raw retrieved chunks (for debugging)
    """
    # ── Retrieve relevant chunks ───────────────────────────────────────────────
    chunks = retrieve(question, k=k)

    # ── Build context block ────────────────────────────────────────────────────
    context_parts = [
        f"[Source: {c['source']}]\n{c['text']}"
        for c in chunks
    ]
    context = "\n\n---\n\n".join(context_parts)

    # ── Call Groq ──────────────────────────────────────────────────────────────
    response = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Documents:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.2,   # low = less creative, more grounded
        max_tokens=600,
    )

    answer = response.choices[0].message.content.strip()

    # ── Programmatic source attribution ────────────────────────────────────────
    # This guarantees sources appear even if the LLM forgets to cite.
    seen = set()
    sources = []
    for c in chunks:
        if c["source"] not in seen:
            sources.append(c["source"])
            seen.add(c["source"])

    return {"answer": answer, "sources": sources, "chunks": chunks}


# ── Quick CLI test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_questions = [
        "When should I start applying for summer SWE internships at Big Tech companies?",
        "What does Microsoft's software engineer intern interview process look like?",
        "What is the best restaurant near campus?",   # out-of-domain — should decline
    ]

    for q in test_questions:
        print(f"\n{'═' * 64}")
        print(f"Q: {q}")
        print('─' * 64)
        result = ask(q)
        print(result["answer"])
        print("\nSources retrieved:")
        for s in result["sources"]:
            print(f"  • {s}")
