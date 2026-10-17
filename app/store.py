# Saves unanswered questions and simple usage counts in the data/ folder. No names or personal data are stored.
import json
import os
import re
import threading
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.getenv("CDD_DATA_DIR") or Path(__file__).resolve().parent.parent / "data")
UNANSWERED_FILE = DATA_DIR / "unanswered.jsonl"
STATS_FILE = DATA_DIR / "stats.json"
_lock = threading.Lock()

EMPTY_STATS = {"questions": 0, "answered": 0, "unknown": 0, "personal": 0, "error": 0,
               "thumbs_up": 0, "thumbs_down": 0, "total_seconds": 0.0}


def scrub(question):
    """Remove emails and long numbers (roll numbers, phone numbers) before saving."""
    question = re.sub(r"\S+@\S+", "[removed]", question)
    return re.sub(r"\d{5,}", "[removed]", question)


def log_unanswered(question):
    row = {"question": scrub(question), "asked_at": datetime.now().isoformat(timespec="seconds")}
    with _lock:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with UNANSWERED_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def list_unanswered():
    """Newest first."""
    if not UNANSWERED_FILE.exists():
        return []
    lines = UNANSWERED_FILE.read_text(encoding="utf-8").splitlines()
    return list(reversed([json.loads(l) for l in lines if l.strip()]))


def get_stats():
    if STATS_FILE.exists():
        return {**EMPTY_STATS, **json.loads(STATS_FILE.read_text(encoding="utf-8"))}
    return dict(EMPTY_STATS)


def _update(change):
    with _lock:
        stats = get_stats()
        change(stats)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        STATS_FILE.write_text(json.dumps(stats, indent=2), encoding="utf-8")


def record_question(kind, seconds):
    def change(s):
        s["questions"] += 1
        s["answered" if kind == "answer" else kind] += 1
        s["total_seconds"] = round(s["total_seconds"] + seconds, 2)
    _update(change)


def record_vote(vote):
    key = "thumbs_up" if vote == "up" else "thumbs_down"
    _update(lambda s: s.__setitem__(key, s[key] + 1))
