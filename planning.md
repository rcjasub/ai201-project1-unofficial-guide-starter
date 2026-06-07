# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Student experiences with tech internship recruiting — covering application timelines, resume strategy, interview formats (OA, phone screen, technical), referrals, and offer decisions.

The most useful recruiting intelligence is scattered across Reddit threads, Glassdoor interview reports, campus career wikis, and Blind posts — each platform captures a different slice (raw student frustration on Reddit, structured interview data on Glassdoor, insider salary context on Blind). No single source aggregates all of it, and search engines surface generic HR advice instead of the specific, opinionated, peer-to-peer knowledge students actually need.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Cornell Career — Recruiting Timeline by Career Pathway | Covers full-time vs internship timing differences across Tech, Finance, and Consulting | https://career.cornell.edu/resources/recruiting-timeline-by-career-pathways/ |
| 2 | UFL Career Center — Recruitment Timeline & What to Know | Covers "advanced hiring" strategy, rolling offers, consulting vs tech timelines | https://career.ufl.edu/recruitment-timeline-and-what-should-i-know-before-i-start-to-apply/ |
| 3 | UChicago Career Advancement — Recruiting Timelines | Structured cross-industry breakdown: Finance, Consulting, Advertising | https://careeradvancement.uchicago.edu/career-toolkit/get-recruiting-ready/recruiting-timelines/ |
| 4 | Yale OCS — CS Industry Guide | Big Tech Aug–Nov, startups Feb–May, research Jan–Apr; hiring timeline and prep steps | https://ocs.yale.edu/resources/yale-computer-science-career-guide/ |
| 5 | CodePath Student Career Handbook — Landing a Software Internship | Step-by-step internship search strategy: timeline, applications, referrals | https://raw.githubusercontent.com/codepath/student-career-handbook/master/internship-and-job-search-strategy/landing-software-internship.md |
| 6 | Tippie School of Business — TCS Recruiting Timelines PDF | Accounting/IB start 12–18 months early; useful contrast with tech recruiting pace | https://students.tippie.uiowa.edu/sites/students.tippie.uiowa.edu/files/2025-08/TCS-Recruiting-Timelines.pdf |
| 7 | Glassdoor — Microsoft SWE Intern Interview Reviews | 554 interviews; behavioral + technical (LC medium), avg 38 days to hire | https://www.glassdoor.com/Interview/Microsoft-Software-Engineer-Internship-Interview-Questions-EI_IE1651.0,9_KO10,38.htm |
| 8 | Glassdoor — LinkedIn SWE Intern Interview Reviews | OA → phone screen → super day; 2 LC mediums; 22 days avg | https://www.glassdoor.com/Interview/LinkedIn-Software-Engineer-Intern-Interview-Questions-EI_IE34865.0,8_KO9,33.htm |
| 9 | Glassdoor — Atlassian SWE Intern Interview Reviews | OA + live coding; 27 days avg; 89% positive experience | https://www.glassdoor.com/Interview/Atlassian-Software-Engineer-Intern-Interview-Questions-EI_IE115699.0,9_KO10,34.htm |
| 10 | Glassdoor — Salesforce SWE Intern Interview Reviews | 46 days avg (longest pipeline); 84% positive; LC pattern-based questions | https://www.glassdoor.com/Interview/Salesforce-Software-Engineer-Intern-Interview-Questions-EI_IE11159.0,10_KO11,35.htm |
| 11 | Glassdoor — IBM SWE Intern Interview Reviews | OA + manager interview; Python/SQL/git questions; less LC-heavy than FAANG | https://www.glassdoor.com/Interview/IBM-Software-Engineer-Intern-Interview-Questions-EI_IE354.0,3_KO4,28.htm |
| 12 | Penn State CS Resource Guide — Interview Prep | Start with easy LeetCode Qs, filtering by type and difficulty | https://sites.psu.edu/csresourceguide/interview-prep |
| 13 | CodePath Student Career Handbook — Technical Interviewing Guide | Q&A guide: interview types (algorithms, behavioral, domain), prep strategy, what to expect | https://raw.githubusercontent.com/codepath/student-career-handbook/master/technical-interviewing/technical-interviewing-guide.md |

---

## Chunking Strategy

**Chunk size:** Mixed — ~100–150 tokens for Glassdoor review blurbs; ~250–400 tokens for career center guide sections; one Q+A pair per chunk for long conversational guides.

**Overlap:** 50 tokens overlap for career center guides (sections sometimes share context across headers); no overlap needed for self-contained review snippets or Q+A pairs.

**Reasoning:** Documents fall into three structural types. Glassdoor reviews (docs 7–11) are short, dense snippets where each candidate anecdote is a natural atomic unit — small chunks preserve the signal without diluting it. Career center guides (docs 1–6) use headers by industry or season; chunking at the section level keeps each chunk topically coherent, and 50-token overlap protects against facts that straddle a section boundary (e.g., a month named at the end of one paragraph with its consequence in the next). The UW Q&A guide (doc 13) is a long conversational page where each question-answer pair is self-contained — treating each pair as one chunk avoids splitting advice mid-thought.

**Signs chunks are too small:** retrieved chunks answer only part of a question and lack the conclusion — e.g., returns "Microsoft has two interview rounds" but not what those rounds contain. **Signs chunks are too large:** the embedding averages over too many topics and stops matching specific queries — e.g., a chunk covering all of finance + consulting + tech timelines won't rank high for a question about Goldman Sachs specifically.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`.

Chosen because it is lightweight and runs locally without API cost, performs strongly on short-to-medium English text (which matches this corpus of reviews and guides), and produces 384-dimensional vectors that ChromaDB handles efficiently. It is also widely documented, making debugging straightforward.

**Top-k:** 5 chunks per query.

A question like "What is Microsoft's intern interview process?" needs 3–4 chunks to cover stages, difficulty rating, and timeline — a single chunk won't contain all of that. Retrieving 10+ chunks risks flooding the prompt with reviews from other companies at similar similarity scores, which degrades answer precision. 5 is the right balance for this corpus size and query specificity.

**Why semantic search finds relevant chunks without exact keyword matches:** embedding models map text into a vector space where meaning proximity equals geometric proximity. A query asking "how hard is the LinkedIn coding interview?" produces a similar vector to a review saying "two LC mediums, back-to-back technical, pretty challenging" — both are about interview difficulty at LinkedIn even though they share no exact words. This is the core advantage over keyword search for opinion-heavy corpora.

**Production tradeoff reflection:** If cost were no constraint, I would evaluate `text-embedding-3-large` (OpenAI) for higher accuracy on nuanced queries, or a model fine-tuned on career/recruiting text. Key tradeoffs to weigh: latency per query, per-token cost at scale, context window length (relevant if chunk sizes grow), and multilingual support (not needed here, but would matter for international student communities).

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | When should I start applying for summer SWE internships at Big Tech companies? | August–November of the prior fall (docs 1, 4, 5) |
| 2 | What does Microsoft's software engineer intern interview process look like, and how hard is it? | Two rounds: one behavioral (1 hour) and one technical (1 hour, LC-medium problems); rated 3/5 difficulty; avg 38 days to hire (doc 7) |
| 3 | How long does it take to get hired as a software engineer intern at LinkedIn on average? | 22 days on average from application to offer (doc 8) |
| 4 | What is the recruiting timeline difference between investment banking and tech internships? | IB/accounting opens 12–18 months early (applications in summer for the following year); tech opens August–November for the following summer — roughly 3–6 months earlier than tech (docs 1, 3, 6) |
| 5 | What do students say about the Salesforce SWE intern interview difficulty and format? | Rated 3/5 difficulty; OA then interview rounds with LC-pattern questions; 84% positive experience; avg 46 days to hire — longest pipeline of the companies reviewed (doc 10) |

Each expected answer contains a specific verifiable fact (a number, a date range, or a named stage) that a grader can check a system response against without subjective judgment.

---

## Anticipated Challenges

1. **Glassdoor content behind a login wall.** Some Glassdoor review pages require authentication to see full text. Scraping may return truncated previews instead of full interview descriptions, leaving chunks with missing information. Mitigation: manually copy-paste full review text as plaintext files before ingestion, saved as `glassdoor_microsoft.txt` etc., and note this limitation in the README.

2. **Cross-document chunk collisions on generic terms.** Queries like "how long does the process take?" could match review chunks from multiple companies at similar similarity scores (Microsoft 38 days, Salesforce 46 days, Atlassian 27 days). The model may blend them without attributing per-company. Mitigation: prepend company name into chunk text itself (not just metadata) so the embedding captures it — e.g., every Microsoft chunk begins with `[Microsoft SWE Intern]`. Surface source metadata in the generated response.

3. **Career center guides are generic and may dilute specific answers.** A query about Salesforce's timeline will correctly retrieve the Glassdoor chunk, but the top-5 may also pull a UChicago guide section that says nothing Salesforce-specific. Mitigation: keep top-k at 5 (not higher) and include a system prompt instruction to prefer specific sourced claims over generic advice when both are present.

4. **Outdated Glassdoor reviews.** A 2022 review may describe a different interview structure than a 2025 review. Mitigation: tag each chunk with the year mentioned in the review text and include it as metadata; surface the date to users in responses where freshness matters.

---

## Architecture

```
Document Ingestion       Chunking              Embedding + Vector Store     Retrieval            Generation
──────────────────       ────────              ────────────────────────     ─────────            ──────────
requests / manual   →   chunk_text()      →   sentence-transformers     →   ChromaDB         →   Claude API
copy-paste              (variable size          all-MiniLM-L6-v2             .query()             (grounded
(13 .txt files)          by doc_type:           384-dim vectors              top-5 chunks         system prompt
                         "review" ~150 tok      stored in ChromaDB           + metadata           w/ source
                         "guide"  ~300 tok      collection on disk           returned)            attribution)
                         "qa"     1 Q+A pair)
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
Give Claude this planning.md (Documents table + Chunking Strategy section) and ask it to implement `ingest.py` with a `chunk_text(text, doc_type)` function that applies different chunk sizes based on `doc_type` (`"review"`, `"guide"`, `"qa"`). Verify output by printing chunk count and average token length per document type before proceeding.

**Milestone 4 — Embedding and retrieval:**
Give Claude the completed Retrieval Approach section plus the output schema of `ingest.py`, and ask it to implement `embed.py` (batch embed all chunks, store to ChromaDB with `source`, `company`, and `year` metadata fields) and `retrieve.py` (embed query → ChromaDB top-5). Verify by running each of the 5 evaluation questions and checking that returned chunks are topically relevant to the question asked.

**Milestone 5 — Generation and interface:**
Give Claude the Grounded Generation section from README.md and ask it to implement `generate.py` with a system prompt that enforces source attribution and instructs the model to prefer specific sourced claims over generic advice. Verify by running all 5 evaluation questions end-to-end and checking that responses cite source documents by name.