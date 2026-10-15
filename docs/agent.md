# agent.md: Rules for the AI Coding Agent

You are helping build **Campus Doubt Desk**, a chatbot that answers student questions from the college handbook.
Read `prd.md` and `roadmap.md` before you write any code. They are the source of truth.

---

## Tech stack

1. **Use only this stack:** Python, FastAPI for the backend, and a simple HTML page for the chat screen. The handbook PDF is in the `data/` folder. Do not add other frameworks (like React) or big libraries without asking first.

## How to work

2. **One phase at a time.** Follow `roadmap.md` in order. Start the next phase only after the current phase's "Done when" condition is met. Tick the `[ ]` boxes in `roadmap.md` as you finish tasks.
3. **Prove it works.** Before you say a phase is done, run its "Done when" check (for example, the 20 test questions) and show the results.

## What to do

4. **Answer only from the handbook.** Never make up an answer, and never use outside knowledge.
5. **Show the page number with every answer.** If you can't find a page number, don't give the answer.
6. **When the answer is not in the handbook, reply with exactly:** "I don't know. Please ask the office."
7. **Keep the code simple.** Small files, clear names, and a one-line comment at the top of every file saying what it does. A beginner should be able to read it.

## What not to do

8. **Don't build anything that is not in `prd.md`.** No extra features. Never build the Non-Goals: login, personal data, admission questions, or general chat.
9. **Keep data and keys safe.** Don't ask for or save student personal data (name, roll number, marks). Never write API keys in the code: keep them in a `.env` file and never push that file to GitHub.

## When in doubt

10. **Ask, don't guess.** If something is unclear, or `prd.md` and `roadmap.md` say different things, stop and ask the PM before you write code.
