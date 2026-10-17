# Decides the reply to a question: a handbook answer with its page number, "I don't know", or a personal-data refusal.
import logging
import re
import time
from urllib.parse import quote

from app import llm, store

IDK = "I don't know. Please ask the office."
PERSONAL = "I can't see personal data like your marks, attendance or fee status. Please contact the college office."
ERROR = "Sorry, I can't answer right now. Please try again in a minute, or ask the office."
DISCLAIMER = "For official decisions, contact the college office."
MAX_LINES = 5

# Questions about the student's own records. The LLM also checks for these.
PERSONAL_PATTERN = re.compile(
    r"^\s*(what('s| is| are| was| were)|show( me)?|tell me|check|how much( is)?|give me)\s+(me\s+)?my\s+"
    r"(marks?|results?|grades?|cgpa|sgpa|scores?|attendance|fee status|fees status|dues|percentage|backlogs?)\b"
    r"|\b(have|did) i (paid|pass(ed)?|fail(ed)?|clear(ed)?)\b|\bam i (detained|passing|failing)\b",
    re.I,
)

SYSTEM_PROMPT = """You answer student questions for Campus Doubt Desk using ONLY the handbook excerpts provided.
Each excerpt starts with its page number, like [Page 9: Attendance Policy].

Rules:
- Use only facts written in the excerpts. Never use outside knowledge and never guess.
- If the excerpts do not directly answer the exact question, the status is "unknown". Information that is only
  related (a different place or service, or a different detail than the one asked) is not an answer.
- If the student asks about their own personal records (their marks, their attendance percentage, whether they
  paid fees, their results), the status is "personal". Questions about the rules themselves are normal questions.
- Questions about admission for new applicants, and anything that is not a college handbook question (jokes,
  coding help, assignments, general chat), are "unknown".
- Write the answer in simple English, in at most 3 short sentences.
- "page" is the page number of the excerpt that contains the answer.

Reply only with JSON: {"status": "answer" | "unknown" | "personal", "answer": "<text or empty>", "page": <number or null>}"""


def ask(question, index, contact):
    """Answer one question and return everything the chat page needs to show."""
    started = time.perf_counter()
    kind, text, page, waited = _decide(question, index)
    seconds = round(time.perf_counter() - started - waited, 2)

    if kind == "unknown":
        store.log_unanswered(question)
    store.record_question(kind, seconds)

    reply = {"type": kind, "answer": text, "page": page, "disclaimer": DISCLAIMER,
             "seconds": seconds, "rate_limit_wait": round(waited, 2)}
    if kind != "answer":
        reply["contact"] = contact
        reply["ask_office_link"] = office_mail_link(contact.get("email"), question)
    return reply


def _decide(question, index):
    if PERSONAL_PATTERN.search(question):
        return "personal", PERSONAL, None, 0.0

    pieces = index.search(question, k=4)
    if not pieces:
        return "unknown", IDK, None, 0.0

    excerpts = "\n\n".join(p["text"] for p in pieces)
    try:
        data, waited = llm.ask_json(SYSTEM_PROMPT, f"Handbook excerpts:\n{excerpts}\n\nStudent question: {question}")
    except Exception:
        logging.exception("LLM call failed")
        return "error", ERROR, None, 0.0

    status = data.get("status")
    answer = str(data.get("answer") or "").strip()
    if status == "personal":
        return "personal", PERSONAL, None, waited

    try:
        page = int(data.get("page"))
    except (TypeError, ValueError):
        page = None
    # No page number from the handbook pieces we sent means no answer (agent.md rule 5).
    if status != "answer" or not answer or page not in {p["page"] for p in pieces}:
        return "unknown", IDK, None, waited
    return "answer", _shorten(answer), page, waited


def _shorten(answer):
    lines = [l.strip() for l in answer.splitlines() if l.strip()]
    return "\n".join(lines[:MAX_LINES])


def office_mail_link(email, question):
    """A mailto: link that opens an email to the office with the question already typed in."""
    subject = "Question from Campus Doubt Desk"
    body = ("Hello,\n\nI could not find the answer to this question in the student handbook:\n\n"
            f"{question}\n\nThank you.")
    return f"mailto:{email or ''}?subject={quote(subject)}&body={quote(body)}"
