# Runs the roadmap "Done when" checks: 20 handbook questions, 5 questions not in the handbook, and a personal-data question.
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["CDD_DATA_DIR"] = tempfile.mkdtemp(prefix="cdd-test-")  # keep test logs out of the real data/ folder

from app import answer, store  # noqa: E402
from main import index, office  # noqa: E402

PACE_SECONDS = 9  # the Groq key allows about 8,000 tokens a minute, so space the calls out
tests = json.loads((ROOT / "tests" / "questions.json").read_text(encoding="utf-8"))


def normalize(text):
    """Lowercase and turn special spaces and hyphens (like non-breaking ones) into plain ones."""
    text = re.sub(r"\s+", " ", text.lower())
    return re.sub(r"[‐-―]", "-", text)


def paced_ask(question):
    started = time.perf_counter()
    reply = answer.ask(question, index, office)
    rest = PACE_SECONDS - (time.perf_counter() - started)
    if rest > 0:
        time.sleep(rest)
    return reply


print("== 20 handbook questions ==")
with_page = correct = fast = 0
for n, t in enumerate(tests["handbook"], 1):
    r = paced_ask(t["q"])
    has_page = r["type"] == "answer" and r["page"] is not None
    right_page = r["page"] in t["pages"]
    has_fact = any(normalize(e) in normalize(r["answer"]) for e in t["expect"])
    ok = has_page and right_page and has_fact
    with_page += has_page
    correct += ok
    fast += r["seconds"] < 10
    print(f"{n:2}. {'PASS' if ok else 'FAIL'} | page {r['page']} (want {t['pages']}) | {r['seconds']:.1f}s | {t['q']}")
    print(f"    -> {r['answer']}")

print("\n== 5 questions not in the handbook ==")
idk_ok = 0
canteen_ok = False
for q in tests["not_in_handbook"]:
    r = paced_ask(q)
    ok = (r["type"] == "unknown" and r["answer"] == answer.IDK and r.get("contact", {}).get("email")
          and r.get("ask_office_link", "").startswith("mailto:") and quote(q) in r["ask_office_link"])
    idk_ok += bool(ok)
    if "canteen menu" in q:
        canteen_ok = r["answer"] == answer.IDK
    print(f"{'PASS' if ok else 'FAIL'} | {r['type']} | {r['answer']} | {q}")

logged = store.list_unanswered()
logged_questions = {row["question"] for row in logged}
log_ok = all(q in logged_questions for q in tests["not_in_handbook"])
fields_ok = all(set(row) == {"question", "asked_at"} for row in logged)

print("\n== Personal data question ==")
r = paced_ask(tests["personal"])
personal_ok = r["type"] == "personal" and "office" in r["answer"].lower()
print(f"{'PASS' if personal_ok else 'FAIL'} | {r['answer']}")

print("\n== Summary (roadmap 'Done when' checks) ==")
checks = [
    (f"Answers with a page number: {with_page}/20", with_page == 20),
    (f"Correct answers (auto-check: right page and key fact): {correct}/20, need 18", correct >= 18),
    (f"Answers under 10 seconds: {fast}/20, need 19", fast >= 19),
    ('"What is the canteen menu today?" says I don\'t know', canteen_ok),
    (f"Not-in-handbook questions show contact + Ask the office link: {idk_ok}/5", idk_ok == 5),
    (f"Unanswered list has all 5 with date and time, no other fields: {log_ok and fields_ok}", log_ok and fields_ok),
    ('"What are my marks?" points to the office', personal_ok),
]
for label, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
print("\nNote: office staff must still check the 20 answers by hand before launch (roadmap Phase 4).")
sys.exit(0 if all(ok for _, ok in checks) else 1)
