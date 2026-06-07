"""
Run once to download the 8 public source documents into documents/.
Glassdoor docs (07–11) must be pasted manually — they require a login.

Usage:
    pip install requests beautifulsoup4
    python fetch_docs.py
"""
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

DOCS_DIR = Path("documents")

SOURCES = [
    ("doc_01_cornell_guide.txt",   "https://career.cornell.edu/resources/recruiting-timeline-by-career-pathways/"),
    ("doc_02_ufl_guide.txt",       "https://career.ufl.edu/recruitment-timeline-and-what-should-i-know-before-i-start-to-apply/"),
    ("doc_03_uchicago_guide.txt",  "https://careeradvancement.uchicago.edu/career-toolkit/get-recruiting-ready/recruiting-timelines/"),
    ("doc_04_yale_guide.txt",      "https://ocs.yale.edu/resources/yale-computer-science-career-guide/"),
    # doc_05: replaced Substack (UK life sciences) with CodePath internship strategy guide
    ("doc_05_codepath_internship_guide.txt", "https://raw.githubusercontent.com/codepath/student-career-handbook/master/internship-and-job-search-strategy/landing-software-internship.md"),
    ("doc_12_pennstate_guide.txt", "https://sites.psu.edu/csresourceguide/interview-prep"),
    # doc_13: replaced UW login-walled page with CodePath technical interviewing guide
    ("doc_13_codepath_interview_qa.txt", "https://raw.githubusercontent.com/codepath/student-career-handbook/master/technical-interviewing/technical-interviewing-guide.md"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; student-project/1.0)"}


def fetch_text(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    # Raw GitHub/text URLs — no HTML to parse
    if "raw.githubusercontent.com" in url or r.headers.get("Content-Type", "").startswith("text/plain"):
        text = re.sub(r"\n{3,}", "\n\n", r.text)
        return text.strip()

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()

    main = (
        soup.find("main")
        or soup.find(attrs={"role": "main"})
        or soup.find("article")
        or soup.find("div", class_=re.compile(r"content|body|post|entry", re.I))
        or soup.body
    )

    text = (main or soup).get_text(separator="\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    for filename, url in SOURCES:
        dest = DOCS_DIR / filename
        if dest.exists() and dest.stat().st_size > 500:
            print(f"SKIP  {filename} (already downloaded)")
            continue
        try:
            text = fetch_text(url)
            dest.write_text(text, encoding="utf-8")
            print(f"OK    {filename} — {len(text):,} chars")
        except Exception as e:
            print(f"FAIL  {filename} — {e}")
            print(f"      Manually paste content from: {url}")


if __name__ == "__main__":
    main()
