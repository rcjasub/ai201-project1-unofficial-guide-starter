# The Unofficial Guide — Project 1

---

## Domain

Student experiences with tech internship recruiting — covering application timelines, resume strategy, interview formats (OA, phone screen, technical), referrals, and offer decisions. This knowledge is valuable because official career center advice is generic and sanitized — it doesn't reflect actual company timelines, which pipelines ghost applicants, or how competitive each process really is. The most useful, opinionated intelligence lives scattered across Glassdoor interview reports, university career wikis, and student guides that most people never find until they're already behind.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Cornell Career — Recruiting Timeline by Career Pathway | Structured guide | https://career.cornell.edu/resources/recruiting-timeline-by-career-pathways/ |
| 2 | UFL Career Center — Recruitment Timeline | Medium guide | https://career.ufl.edu/recruitment-timeline-and-what-should-i-know-before-i-start-to-apply/ |
| 3 | UChicago Career Advancement — Recruiting Timelines | Structured page | https://careeradvancement.uchicago.edu/career-toolkit/get-recruiting-ready/recruiting-timelines/ |
| 4 | Yale OCS — CS Industry Guide | Short guide | https://ocs.yale.edu/resources/yale-computer-science-career-guide/ |
| 5 | CodePath Student Career Handbook — Landing a Software Internship | GitHub markdown guide | https://raw.githubusercontent.com/codepath/student-career-handbook/master/internship-and-job-search-strategy/landing-software-internship.md |
| 6 | Glassdoor — Microsoft SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/Microsoft-Software-Engineer-Internship-Interview-Questions-EI_IE1651.0,9_KO10,38.htm |
| 7 | Glassdoor — LinkedIn SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/LinkedIn-Software-Engineer-Intern-Interview-Questions-EI_IE34865.0,8_KO9,33.htm |
| 8 | Glassdoor — Atlassian SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/Atlassian-Software-Engineer-Intern-Interview-Questions-EI_IE115699.0,9_KO10,34.htm |
| 9 | Glassdoor — Salesforce SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/Salesforce-Software-Engineer-Intern-Interview-Questions-EI_IE11159.0,10_KO11,35.htm |
| 10 | Glassdoor — IBM SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/IBM-Software-Engineer-Intern-Interview-Questions-EI_IE354.0,3_KO4,28.htm |
| 11 | Penn State CS Resource Guide — Interview Prep | Short how-to page | https://sites.psu.edu/csresourceguide/interview-prep |
| 12 | CodePath Student Career Handbook — Technical Interviewing Guide | GitHub markdown Q&A guide | https://raw.githubusercontent.com/codepath/student-career-handbook/master/technical-interviewing/technical-interviewing-guide.md |

---

## Chunking Strategy

**Chunk size:** Three different sizes depending on document type. Glassdoor review chunks: ~500 characters (~125 tokens) — each candidate anecdote is a natural atomic unit and small chunks preserve the signal without diluting it. Career center guide chunks: ~1,400 characters (~350 tokens) — these are long structured documents with sections per industry; one section per chunk keeps each chunk topically coherent. CodePath Q&A guide chunks: split on markdown headers (## / ###), capped at 1,500 characters — each section is already a self-contained topic so structural boundaries are the natural split point.

**Overlap:** 200 characters (~50 tokens) on guide chunks only. Career center guides sometimes place a month name at the end of one paragraph and its consequence at the start of the next — overlap prevents that context from being lost at a section boundary. No overlap on review or Q&A chunks because each unit is already self-contained.

**Why these choices fit your documents:** A single fixed chunk size would either fragment the short Glassdoor anecdotes (losing the narrative) or leave the long career guides as unmanageably large blocks that match everything weakly. Matching chunk strategy to document structure ensures each embedded chunk carries one focused idea. Preprocessing: HTML tags, HTML entities (&amp;, &#39;), and excessive whitespace were stripped before chunking. Glassdoor review chunks also received a company-name prefix (e.g. "Microsoft interview review:") to preserve company identity in the embedding, which would otherwise be lost in short chunks.

**Final chunk count:** 74 chunks across 12 documents.

**Sample chunks (5 labeled):**

*Chunk 1 — doc_07_glassdoor_microsoft.txt (type: review)*
> Microsoft interview review: I interviewed at Microsoft. Interview. The hiring process consists of a HackerRank home exam, followed by three technical interviews covering LeetCode-style problems and system architecture. Once this is done, you will have a final HR interview. Interview questions. Question 1. I had a technical interview where I was asked to solve the classic 'Climbing Stairs' problem (LeetCode #70), which is a dynamic programming question based on the Fibonacci sequence.

*Chunk 2 — doc_09_glassdoor_atlassian.txt (type: review)*
> Atlassian interview review: I interviewed at Atlassian (Sydney). Interview. The process started with an online assessment (OA), which was reasonably balanced in difficulty. Candidates who passed were invited to a live coding interview conducted over Zoom with a software engineer. The interview focused on data structures and algorithms, with an emphasis on problem-solving approach, code clarity, and communication throughout the solution.

*Chunk 3 — doc_12_codepath_interview_qa.txt (type: qa)*
> ### The three types of internship interviews. Internship interviews tend to fall into one of three categories: 1. The programming interview: algorithms, data structures, coding. 2. The "what you've done interview": you and your projects. 3. The domain-specific interview: quizzed about a tech stack you claim to know. We'll explain these in more depth below.

*Chunk 4 — doc_05_codepath_internship_guide.txt (type: guide)*
> ### 1. Start the search early. You can start by listing all the companies whose products you used or enjoyed, and then searching "software engineering intern" on the sites and sifting through those listings for companies or posts that sound interesting. The following sites have internship listings: LinkedIn, Indeed, Handshake, Glassdoor, and company career pages directly.

*Chunk 5 — doc_01_cornell_guide.txt (type: guide)*
> Computing, Information Science, and Tech. Jobs | February – November. Larger firms with established programs will fill roles in the late summer or early fall for positions beginning the following year. Internships | August – February. Larger tech organizations also offer early engagement programs for first and second year students.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`. Chosen because it runs entirely locally with no API key or rate limits, is fast enough to embed 74 chunks in under 2 seconds on CPU, and produces 384-dimensional vectors that ChromaDB handles efficiently. It performs strongly on short-to-medium English text, which matches this corpus of reviews and guides.

**Production tradeoff reflection:** If deploying for real users with no cost constraint, the key tradeoffs to weigh would be: (1) **Accuracy on domain-specific text** — a model fine-tuned on career or recruiting text would better understand phrases like "super day," "OA," or "return offer" that carry specific meaning in this domain. (2) **Context length** — all-MiniLM-L6-v2 has a 256-token limit, which means longer chunks get truncated; a model like `text-embedding-3-large` (OpenAI) supports much longer inputs. (3) **Latency vs. accuracy** — larger models produce better embeddings but are slower; for a real-time UI, latency matters. (4) **Local vs. API-hosted** — local models have no per-query cost but require compute infrastructure; API-hosted models scale easily but add cost and a network dependency.

---

## Retrieval Test Results

**Query 1: "When should I start applying for summer SWE internships at Big Tech companies?"**

| Rank | Source | Distance | Why relevant |
|------|--------|----------|--------------|
| 1 | doc_05_codepath_internship_guide.txt | 0.3312 | Directly mentions "late August or early September" as the recommended start time |
| 2 | doc_02_ufl_guide.txt | 0.3541 | Covers campus recruiting timeline overview and when companies begin accepting applications |
| 3 | doc_02_ufl_guide.txt | 0.3902 | Specifically states employers "release their next year of internship opportunities towards end of Aug or early Sep" |

All three results are on-topic and contain the specific timing information needed to answer the question.

**Query 2: "What does Microsoft's software engineer intern interview process look like?"**

| Rank | Source | Distance | Why relevant |
|------|--------|----------|--------------|
| 1 | doc_12_codepath_interview_qa.txt | 0.3484 | General SWE internship interview guide — relevant to process but not Microsoft-specific |
| 2 | doc_12_codepath_interview_qa.txt | 0.3746 | Attribution chunk — not useful content |
| 3 | doc_06_glassdoor_microsoft.txt | 0.4064 | Microsoft-specific review describing HackerRank exam + three technical rounds |

The Microsoft chunk reached position 3 only after adding a company-name prefix to review chunks. Without the prefix, the Microsoft chunk did not appear in the top 5 — see Failure Case Analysis.

**Query 3: "How many LeetCode problems do I need to solve before I'm ready to interview?"**

| Rank | Source | Distance | Why relevant |
|------|--------|----------|--------------|
| 1 | doc_11_pennstate_guide.txt | 0.3650 | Directly addresses LeetCode — recommends the "Blind 75" list and advises against solving all 2,500 |
| 2 | doc_06_glassdoor_microsoft.txt | 0.4156 | Microsoft review mentions LeetCode-style problems in the interview |
| 3 | doc_12_codepath_interview_qa.txt | 0.4728 | Ex-Facebook interviewer tips on how to approach coding problems |

Strong retrieval — the Penn State guide is the most directly relevant source and ranks first.

---

## Grounded Generation

**System prompt grounding instruction:** The system prompt uses hard constraint language rather than suggestions:

> *"You must answer the user's question using ONLY the information in the documents provided below. Do not use any outside knowledge or training data — even if you know the answer from elsewhere. If the provided documents do not contain enough information to answer the question, respond with exactly: 'I don't have enough information in my documents to answer that.'"*

The words "must," "ONLY," and "Do not" are load-bearing — vague instructions like "try to use the documents" leave the model room to fill gaps with training data. The instruction to respond with an exact phrase when information is missing was verified: an out-of-domain question produced that exact refusal.

**How source attribution is surfaced in the response:** Attribution is enforced in two layers. First, the system prompt instructs the model to cite the source filename in its answer (e.g. "According to doc_02_ufl_guide.txt..."). Second, the `ask()` function in `generate.py` programmatically appends the list of retrieved source filenames to every response regardless of whether the LLM cites — this guarantees attribution is always present. The Gradio UI displays these sources in a separate "Retrieved from" box below the answer.

**Example responses:**

*Example 1 — grounded response with citation:*
> Query: "When should I start applying for summer SWE internships at Big Tech companies?"
>
> Response: "According to doc_13_codepath_interview_qa.txt, most internship applications start popping up in October and November. Additionally, doc_02_ufl_guide.txt mentions that larger corporations and employers usually release their next year's internship opportunities towards the end of August or early September. Therefore, it is recommended to start applying for summer SWE internships at Big Tech companies in August or September, but definitely by October and November."
>
> Sources retrieved: doc_05_codepath_internship_guide.txt, doc_02_ufl_guide.txt, doc_12_codepath_interview_qa.txt, doc_01_cornell_guide.txt

*Example 2 — grounded response with citation:*
> Query: "What does Microsoft's software engineer intern interview process look like?"
>
> Response: "According to doc_07_glassdoor_microsoft.txt, Microsoft's software engineer intern interview process consists of a HackerRank home exam, followed by three technical interviews covering LeetCode-style problems and system architecture, and finally an HR interview."
>
> Sources retrieved: doc_12_codepath_interview_qa.txt, doc_06_glassdoor_microsoft.txt, doc_11_glassdoor_ibm.txt

*Example 3 — out-of-scope refusal:*
> Query: "What is the best restaurant near campus?"
>
> Response: "I don't have enough information in my documents to answer that."

---

## Query Interface

**Input field:** A text box labeled "Your question" with placeholder text showing an example query. Supports both clicking the "Ask" button and pressing Enter to submit.

**Output fields:** Two text boxes displayed below the input — "Answer" (10 lines, showing the LLM's grounded response with inline source citations) and "Retrieved from" (4 lines, listing the source filenames the system pulled from).

**Sample interaction transcript:**

```
User input:
  What's the difference in recruiting timelines between finance and tech internships?

Answer box:
  According to doc_01_cornell_guide.txt and doc_03_uchicago_guide.txt, the recruiting
  timelines for finance/banking internships and tech internships differ significantly.

  In finance and banking, internships typically recruit a year in advance, with many
  large financial institutions recruiting sophomores for junior year summer internships.
  Third-year internship recruiting for investment banking and private equity firms
  begins in the fall of a student's second year.

  In contrast, tech internships typically recruit in the summer and early fall, with
  larger tech organizations offering early engagement programs for first and second-year
  students. Finance/banking internships tend to have earlier recruiting timelines,
  often starting in the fall or even earlier, while tech internships typically start
  recruiting in the summer or early fall.

Retrieved from box:
  • doc_01_cornell_guide.txt
  • doc_03_uchicago_guide.txt
  • doc_02_ufl_guide.txt
  • doc_05_codepath_internship_guide.txt
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | When should I start applying for summer SWE internships at Big Tech? | August–November of the prior fall | "Recommended to start in August or September, but definitely by October and November" — cited doc_05 and doc_02 | Relevant | Accurate |
| 2 | What does Microsoft's SWE intern interview process look like? | Behavioral + LC medium problems, ~38 days to hire | "HackerRank home exam, three technical interviews covering LeetCode-style problems and system architecture, then HR interview" — cited doc_07 | Partially relevant (general guide ranked above Microsoft chunk) | Partially accurate (process correct; 38-day timeline not in docs) |
| 3 | How many LeetCode problems do I need before I'm ready to interview? | No specific number; focus on pattern recognition, filter by type | "Not necessary to solve all 2,500 — start with easy questions, filter for Blind 75 — no specific number given" — cited doc_12 | Relevant | Accurate |
| 4 | Should I apply through LinkedIn or company job portals directly? | Both useful; portals reduce ATS friction, LinkedIn useful for referrals | "Apply through both LinkedIn and company career website for broader opportunities" — cited doc_02 | Relevant | Accurate |
| 5 | What's the difference in recruiting timelines between finance and tech internships? | Finance starts 12–18 months early; tech is August–November for following summer | "Finance recruits a year in advance, often starting sophomore year; tech recruits in summer/early fall" — cited doc_01 and doc_03 | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** "What does Microsoft's software engineer intern interview process look like?"

**What the system returned:** In the initial version, the system returned a general technical interviewing guide (doc_12_codepath_interview_qa.txt) and an IBM review (doc_11_glassdoor_ibm.txt) in the top results — the Microsoft Glassdoor document did not appear at all. After the fix, the Microsoft chunk moved to position 3, but a general interview guide and a useless attribution chunk ("This post is adapted from...") still ranked above it.

**Root cause (tied to a specific pipeline stage):** The failure originated in the **chunking and embedding stages**. The Microsoft review chunks contained interview descriptions ("HackerRank exam," "three technical interviews," "LeetCode-style problems") but did not repeat the word "Microsoft" in the body of the chunk — only in the introductory header line that was merged in. The `all-MiniLM-L6-v2` embedding model mapped these chunks based primarily on their interview content words, which are identical across all company review chunks. Because the company identity signal was absent from the embedding, the model could not distinguish Microsoft chunks from IBM or Atlassian chunks when given a Microsoft-specific query.

**What you would change to fix it:** A company-name prefix ("Microsoft interview review:") was added to every Glassdoor review chunk before embedding, injecting the company name directly into the text the model encodes. This moved the Microsoft chunk into the top 3. A more thorough fix would be to collect more Microsoft-specific reviews — with only 3 short reviews in the corpus, the Microsoft signal is still underrepresented relative to the larger general guides. Additionally, the attribution chunk ("This post is adapted from...") should be filtered out during ingestion, as it carries no useful information but still consumes a retrieval slot.

---

## Spec Reflection

**One way the spec helped you during implementation:** The chunking strategy section of planning.md forced the decision about document types before any code was written. Because the three types (review, guide, qa) were identified in the spec with explicit size rationale, the implementation could use separate strategies for each rather than a single fixed split. Without the spec, the default would have been one uniform chunk size — which would have either fragmented the short Glassdoor anecdotes or left the long career center guides as unmanageably large blocks. The spec made the three-strategy design feel inevitable rather than complex.

**One way your implementation diverged from the spec, and why:** Two of the planned source documents had to be replaced during implementation. The UW resume guide (source 13 in the original spec) was behind a university login wall and returned only a login-page HTML fragment instead of the article. The Substack article (source 5) turned out to be about UK life sciences internships, not US tech recruiting — a domain mismatch that wasn't detectable from the URL alone. Both were replaced with publicly accessible GitHub-hosted markdown files from the CodePath student career handbook. The spec described what types of content to look for, but could not predict which specific URLs would actually be accessible or on-topic.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Documents section and Chunking Strategy section from planning.md, describing three document types (review, guide, qa) with different chunk sizes (125 tokens, 350 tokens, header-based), plus the pipeline architecture diagram.
- *What it produced:* A complete `ingest.py` with `load_documents()`, `clean_text()`, `get_doc_type()`, and separate chunking functions for each document type, plus a `run_pipeline()` function that prints 5 sample chunks and total chunk count for inspection.
- *What I changed or overrode:* The initial version used a simple paragraph split for all document types. I directed the AI to implement word-boundary snapping in the guide chunker (so chunks never start mid-word) and to add a minimum-length merge step in the review chunker (so short metadata lines like "I interviewed at Microsoft" don't become standalone 53-character chunks). I also directed it to add a company-name prefix function after observing that Microsoft-specific queries were returning IBM and Atlassian results.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section from planning.md (embedding model: all-MiniLM-L6-v2, top-k: 5, vector store: ChromaDB), the pipeline diagram, and the output of ingest.py showing 74 chunks with metadata.
- *What it produced:* `embed.py` (loads chunks, embeds with sentence-transformers, stores in ChromaDB with cosine distance metric) and `retrieve.py` (query → embed → ChromaDB search → return top-k with source and distance score), plus a test harness running 3 evaluation questions and printing results.
- *What I changed or overrode:* The initial version used ChromaDB's default L2 distance metric, which produced scores in the 0.6–0.9 range that appeared to fail the milestone's "below 0.5" threshold. I directed the AI to switch to cosine distance (`metadata={"hnsw:space": "cosine"}`) so scores align with the 0–1 range the milestone guidance is calibrated for. I also directed it to add the company-prefix fix to `ingest.py` after observing the Microsoft retrieval failure in the retrieve.py test output.
