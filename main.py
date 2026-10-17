# Starts the Campus Doubt Desk web app: chat page, ask API, feedback buttons and the unanswered-questions list.
from html import escape
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from app import answer, contacts, handbook, search, store

ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "data" / "handbook.pdf"

# Load the handbook once when the server starts.
pages = handbook.read_pages(PDF_PATH)
problems = handbook.check_readable(pages)
if problems:
    print("WARNING: handbook text problems:", problems)
index = search.Index(search.make_chunks(pages))
office = contacts.find_office_contact(pages)

SUGGESTED = [
    "What is the minimum attendance?",
    "When is the last date to pay fees?",
    "How do I apply for re-evaluation?",
    "What are the library timings?",
    "How much does a duplicate ID card cost?",
]

app = FastAPI(title="Campus Doubt Desk")

# Lets the chat page served separately on port 5500 call this backend on port 8000.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class Vote(BaseModel):
    vote: Literal["up", "down"]


@app.get("/")
def chat_page():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api/suggested")
def suggested():
    return SUGGESTED


@app.post("/api/ask")
def ask(body: Question):
    text = body.question.strip()
    if not text:
        raise HTTPException(400, "Please type a question.")
    return answer.ask(text, index, office)


@app.post("/api/feedback")
def feedback(body: Vote):
    store.record_vote(body.vote)
    return {"ok": True}


@app.get("/api/unanswered")
def unanswered_json():
    return store.list_unanswered()


@app.get("/api/health")
def health():
    return {"pages": len(pages), "pieces": len(index.chunks), "problems": problems, "office": office}


@app.get("/unanswered", response_class=HTMLResponse)
def unanswered_page():
    """Simple list for office staff and the PM to review once a week."""
    s = store.get_stats()
    votes = s["thumbs_up"] + s["thumbs_down"]
    up_rate = f"{100 * s['thumbs_up'] / votes:.0f}%" if votes else "-"
    idk_rate = f"{100 * s['unknown'] / s['questions']:.0f}%" if s["questions"] else "-"
    avg = f"{s['total_seconds'] / s['questions']:.1f} s" if s["questions"] else "-"
    rows = "".join(
        f"<tr><td>{escape(r['asked_at'].replace('T', ' '))}</td><td>{escape(r['question'])}</td></tr>"
        for r in store.list_unanswered()
    ) or '<tr><td colspan="2">No unanswered questions yet.</td></tr>'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Unanswered Questions</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f4f6fb;color:#1d2433}}
h1{{font-size:20px;margin:0 0 4px}} p{{color:#5b6475;margin:0 0 16px;font-size:14px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin-bottom:16px}}
.stat{{background:#fff;border:1px solid #dde2ec;border-radius:8px;padding:10px}}
.stat b{{display:block;font-size:20px}} .stat span{{font-size:12px;color:#5b6475}}
table{{width:100%;border-collapse:collapse;background:#fff;font-size:14px}}
td,th{{border:1px solid #dde2ec;padding:8px;text-align:left;overflow-wrap:anywhere}} th{{background:#eef1f8}}
</style></head><body>
<h1>Unanswered questions</h1>
<p>Questions the bot could not answer from the handbook. Only the question and time are saved. Review weekly.</p>
<div class="stats">
<div class="stat"><b>{s['questions']}</b><span>Questions asked</span></div>
<div class="stat"><b>{s['unknown']} ({idk_rate})</b><span>"I don't know" answers</span></div>
<div class="stat"><b>{s['thumbs_up']} / {s['thumbs_down']}</b><span>Thumbs up / down</span></div>
<div class="stat"><b>{up_rate}</b><span>Thumbs-up rate</span></div>
<div class="stat"><b>{avg}</b><span>Average answer time</span></div>
</div>
<table><tr><th>Date and time</th><th>Question</th></tr>{rows}</table>
</body></html>"""
