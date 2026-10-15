# Roadmap: Campus Doubt Desk

Based on `prd.md`. We build in 5 small phases (Phase 5 was added after v1 testing).

**Rule:** Finish one phase fully before starting the next. If something breaks, we know which phase caused it.

---

## Phase 1: Ask one question, get one answer

The smallest working version. No screen, no design, just proof that it works.

- [ ] Put the handbook PDF in the `data/` folder
- [ ] Read the text from the PDF
- [ ] Check that the text is readable (not broken or empty)
- [ ] Break the text into small pieces so the bot can search it
- [ ] Ask one question: "What is the minimum attendance?"
- [ ] Get an answer that comes from the handbook

**Done when:** We ask "What is the minimum attendance?" and get the correct answer from the handbook.

---

## Phase 2: Page numbers and "I don't know"

Make the answers correct and safe.

- [ ] Remember the page number of every piece of text
- [ ] Show the page number with every answer
- [ ] If the answer is not in the handbook, say: "I don't know. Please ask the office."
- [ ] If someone asks for personal data (marks, fees status), say the bot can't see it and point them to the office
- [ ] Keep every answer to 5 lines or less
- [ ] Write 20 test questions, each with the right answer and page number

**Done when:**
- All 20 test questions get an answer with a page number
- At least 18 of the 20 answers are correct
- "What is the canteen menu today?" gets "I don't know. Please ask the office."
- "What are my marks?" points the student to the office

---

## Phase 3: Simple chat screen

Now a student can use it, not just us.

- [ ] Make a chat page with a text box and a "Send" button
- [ ] Show the answer with its page number
- [ ] Add a line under every answer: "For official decisions, contact the college office."
- [ ] Show "Thinking..." while the answer is loading
- [ ] Make the page work on a phone screen
- [ ] Check the speed of all 20 test questions

**Done when:** A student opens the link on a phone, asks a question, and sees the answer with a page number. 19 of 20 answers come in under 10 seconds, with no side-scrolling.

---

## Phase 4: Suggested questions and polish

Make it easy to start and easy to measure.

- [ ] Show 4-5 suggested questions (for example, "What is the minimum attendance?")
- [ ] Add thumbs up / thumbs down on every answer
- [ ] Save the thumbs up / down counts so we can track success
- [ ] Office staff run the 20-question test and mark each answer right or wrong
- [ ] Fix the wrong answers they find
- [ ] Let 5 students try it and fix anything that confuses them

**Done when:** Office staff sign off (at least 18 of 20 answers correct), suggested questions work, thumbs up / down counts are saved, and the bot is ready for the first 50 students.

---

## Phase 5: Help when the bot doesn't know

Added after v1 testing (see the new requirement in `prd.md`). Students who got "I don't know" had nowhere to go next.

- [ ] When the bot says "I don't know", also show the office phone, email, and timings (from the handbook's contacts page)
- [ ] Add an "Ask the office" button under that answer
- [ ] Make the button open an email to the office with the student's question already typed in
- [ ] Save every unanswered question with the date and time (no name or personal data)
- [ ] Make a simple list where office staff and the PM can see these questions
- [ ] Test with 5 questions that are not in the handbook

**Done when:**
- All 5 test questions show the office contact and the "Ask the office" button
- The button opens an email with the question already filled in
- All 5 questions appear in the unanswered list with date and time, and no personal data is saved

---

## Not in this roadmap

These are "Later" in the PRD. We pick them up only after Phase 5 is done:

- Questions in Hindi or Hinglish
- A WhatsApp version
- Easy update when a new handbook comes out
