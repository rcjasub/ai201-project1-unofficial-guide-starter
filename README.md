# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

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
| 5 | Industry Aware (Substack) — Timing for Internships | Long article | https://industryaware.substack.com/p/timing-for-internships-when-to-apply |
| 6 | Tippie Business School — TCS Recruiting Timelines PDF | PDF | https://students.tippie.uiowa.edu/sites/students.tippie.uiowa.edu/files/2025-08/TCS-Recruiting-Timelines.pdf |
| 7 | Glassdoor — Microsoft SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/Microsoft-Software-Engineer-Internship-Interview-Questions-EI_IE1651.0,9_KO10,38.htm |
| 8 | Glassdoor — LinkedIn SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/LinkedIn-Software-Engineer-Intern-Interview-Questions-EI_IE34865.0,8_KO9,33.htm |
| 9 | Glassdoor — Atlassian SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/Atlassian-Software-Engineer-Intern-Interview-Questions-EI_IE115699.0,9_KO10,34.htm |
| 10 | Glassdoor — Salesforce SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/Salesforce-Software-Engineer-Intern-Interview-Questions-EI_IE11159.0,10_KO11,35.htm |
| 11 | Glassdoor — IBM SWE Intern Interview Reviews | Review aggregator | https://www.glassdoor.com/Interview/IBM-Software-Engineer-Intern-Interview-Questions-EI_IE354.0,3_KO4,28.htm |
| 12 | Penn State CS Resource Guide — Interview Prep | Short how-to page | https://sites.psu.edu/csresourceguide/interview-prep |
| 13 | UW CSE — Kim's Ultimate Guide to Building Your Resume | Long Q&A guide | https://ugradnews.cs.washington.edu/2019/09/09/kims-ultimate-guide-to-building-your-resume |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
