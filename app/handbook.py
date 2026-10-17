# Reads the handbook PDF, cleans each page's text, and checks that the text is readable.
import re
from collections import Counter

from pypdf import PdfReader

PAGE_FOOTER = re.compile(r"^page\s+\d+(\s+of\s+\d+)?$", re.I)
SECTION_LINE = re.compile(r"^section\s+\d+$", re.I)


def read_pages(pdf_path):
    """Return one {"page", "title", "text"} dict per PDF page. Page numbers start at 1."""
    reader = PdfReader(str(pdf_path))
    raw = [[line.strip() for line in (page.extract_text() or "").splitlines()] for page in reader.pages]

    # Header lines that repeat on most pages add nothing to search, so drop them.
    counts = Counter(line for lines in raw for line in set(lines) if line)
    repeated = {line for line, n in counts.items() if len(raw) > 2 and n > len(raw) / 2}

    pages = []
    for number, lines in enumerate(raw, start=1):
        kept = [l for l in lines if l and l not in repeated and not PAGE_FOOTER.match(l)]
        pages.append({"page": number, "title": _title(kept), "text": _join_bullets(kept)})
    return pages


def check_readable(pages):
    """Return a list of problems with the extracted text (an empty list means it looks fine)."""
    problems = []
    total = sum(len(p["text"]) for p in pages)
    if total < 500:
        problems.append(f"Only {total} characters of text found. The PDF may be scanned images.")
    thin = [p["page"] for p in pages if len(p["text"]) < 30]
    if thin:
        problems.append(f"Pages with almost no text: {thin}")
    return problems


def _title(lines):
    if len(lines) > 1 and SECTION_LINE.match(lines[0]):
        return lines[1]
    return lines[0] if lines else ""


def _join_bullets(lines):
    """Turn a lone bullet-symbol line plus the next line into one '- text' line."""
    out, bullet = [], False
    for line in lines:
        if len(line) == 1 and not line.isalnum():
            bullet = True
            continue
        out.append(f"- {line}" if bullet else line)
        bullet = False
    return "\n".join(out)
