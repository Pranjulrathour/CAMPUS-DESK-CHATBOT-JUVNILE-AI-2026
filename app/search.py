# Breaks handbook pages into small pieces and finds the pieces that best match a question (BM25 keyword search).
import math
import re
from collections import Counter

STOPWORDS = set("""a an the is are was were be been am to of in on at for and or but what when where how who whom
which why do does did doing i my me mine we our you your it its this that these those there here with by from as
about much many any have has had will would should could can may might must please tell know get got if then than
so not no yes up out into over under again also just only very more most some such own same too each other""".split())

# Extra words to search for when a question uses a different word than the handbook.
SYNONYMS = {
    "deadline": ["last", "date", "due"], "penalty": ["fine", "late"], "timing": ["hour", "open"],
    "timings": ["hour", "open"], "time": ["hour", "open"], "cost": ["fee", "inr"], "price": ["fee", "inr"],
    "charge": ["fee", "inr"], "exam": ["examination"], "examination": ["exam"], "pay": ["payment", "fee"],
    "lose": ["lost", "duplicate"], "lost": ["duplicate"], "curfew": ["gate"], "pass": ["passing"],
    "absent": ["absence", "leave"],
}


def stem(word):
    """Very small stemmer so 'fees'/'fee' and 'borrowing'/'borrow' match."""
    for suffix in ("ing", "ed"):
        if word.endswith(suffix) and len(word) > len(suffix) + 3:
            word = word[: -len(suffix)]
    for suffix in ("s", "e"):
        if word.endswith(suffix) and len(word) > 3:
            word = word[:-1]
    return word


def tokenize(text):
    words = re.findall(r"[a-z0-9]+(?:[.:][0-9]+)?", text.lower())
    return [stem(w) for w in words if w not in STOPWORDS]


def question_words(question):
    raw = [w for w in re.findall(r"[a-z0-9]+(?:[.:][0-9]+)?", question.lower()) if w not in STOPWORDS]
    extra = [s for w in raw for s in SYNONYMS.get(w, [])]
    return {stem(w) for w in raw + extra}


def make_chunks(pages, size=700):
    """Split every page into pieces of about `size` characters. Each piece remembers its page number."""
    chunks = []
    for page in pages:
        piece = []
        for line in page["text"].splitlines():
            piece.append(line)
            if sum(len(l) for l in piece) >= size:
                chunks.append(_chunk(page, piece))
                piece = []
        if piece:
            chunks.append(_chunk(page, piece))
    return chunks


def _chunk(page, lines):
    header = f"[Page {page['page']}: {page['title']}]"
    return {"page": page["page"], "title": page["title"], "text": header + "\n" + "\n".join(lines)}


class Index:
    """Keyword index over handbook pieces."""

    def __init__(self, chunks, k1=1.2, b=0.75):
        self.chunks = chunks
        self.k1, self.b = k1, b
        # The page title is counted twice so a question about "hostel" finds every piece of the hostel page.
        self.terms = [Counter(tokenize(c["text"]) + tokenize(c["title"])) for c in chunks]
        self.lengths = [sum(t.values()) for t in self.terms]
        self.avg_length = sum(self.lengths) / max(len(self.lengths), 1)
        doc_freq = Counter(word for t in self.terms for word in t)
        n = len(chunks)
        self.idf = {w: math.log(1 + (n - df + 0.5) / (df + 0.5)) for w, df in doc_freq.items()}

    def search(self, question, k=4):
        """Return up to k best-matching pieces. An empty list means nothing in the handbook matched."""
        words = question_words(question)
        scored = []
        for i, terms in enumerate(self.terms):
            score = 0.0
            for w in words:
                tf = terms.get(w, 0)
                if tf:
                    norm = tf + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg_length)
                    score += self.idf[w] * tf * (self.k1 + 1) / norm
            if score > 0:
                scored.append((score, i))
        scored.sort(reverse=True)
        return [self.chunks[i] for _, i in scored[:k]]
