# PRD: Campus Doubt Desk

**One line:** A chatbot that answers student questions from the college handbook PDF and shows the page number with every answer.

**Status:** Draft v1 · **Owner:** Product Manager

---

## 1. Problem

- The student handbook is 80 pages long. Almost nobody reads it.
- Students ask seniors or WhatsApp groups instead, and often get wrong answers.
- The same simple questions (attendance, hostel, fees, exams) reach the office every day, so the office is always crowded.
- A wrong answer is not a small thing. A student can miss a fee deadline or an exam form date because of it.

## 2. Users (2 personas)

**Aarav, 18, 1st-year student**
- New to college, lives in the hostel, uses a phone for everything.
- Wants quick answers like "What time does the hostel gate close?"
- Today: asks seniors, gets different answers, then stands in the office line to confirm.

**Mrs. Sharma, college office staff**
- Answers the same 20-30 questions every day.
- Wants fewer repeat questions so she can focus on real work (fee receipts, certificates).
- Needs the bot to give the same answer she would give from the handbook.

## 3. Goal

Help students get the correct handbook answer in seconds, without going to the office.

## 4. Success Metrics (first 30 days after launch)

| Metric | Target |
| --- | --- |
| Questions solved by the bot (student clicks "Yes, this helped") | 60% or more |
| Drop in repeat questions at the office (office tally, 1 week before vs after) | 30% fewer |
| Answers that get a thumbs-up | 80% or more |
| Answers that show a page number | 100% |
| Time to answer | Under 10 seconds |
| Students who use it in week 1 | 50 or more |

## 5. User Stories

1. As a student, I want to ask a question in my own words, so I don't have to read 80 pages.
2. As a student, I want to see the page number with the answer, so I can check it myself.
3. As a student, I want the bot to tell me when it doesn't know, so I don't act on a wrong answer.
4. As office staff, I want students to get simple answers from the bot, so fewer people stand in the line.
5. As office staff, I want the bot's answers to match the handbook, so I don't have to correct wrong information.

## 6. Requirements

**Must (v1)**
- Read the handbook PDF and answer only from it.
- Show the page number with every answer.
- If the answer is not in the handbook, say: "I don't know. Please ask the office."
- Keep answers short (5 lines or less) and in simple English.
- Work on a phone browser.

**Should**
- Show 4-5 suggested questions (for example, "What is the minimum attendance?").
- Thumbs up / thumbs down on every answer.

**Later**
- Questions in Hindi or Hinglish.
- A WhatsApp version.
- Easy update when a new handbook comes out.

**New requirement (Must, added after v1 testing)**

*Why:* The v1 logs showed students asking questions that are not in the handbook. The bot said "I don't know", but the student had nowhere to go next.

- When the bot can't find an answer, show:
  - the office contact: phone, email, and office timings (from the handbook's Important Contacts page)
  - an **"Ask the office"** button that opens an email to the office with the student's question already filled in
- Keep a log of unanswered questions. Save only the question and the date/time. No name, roll number, or other personal data.
- Office staff and the PM can see the list of unanswered questions, and review it once a week.

## 7. Non-Goals (we will NOT build these)

- No login or student accounts.
- No personal data: marks, attendance %, or fee status.
- No admission questions for new applicants.
- No general chat (jokes, assignments, coding help). Handbook questions only.
- No actions like paying fees or applying for leave.

## 8. Acceptance Criteria (testable)

1. Ask "What is the minimum attendance?" and the answer matches the handbook and shows the correct page number.
2. Ask 20 handbook questions: all 20 answers show a page number.
3. Out of those 20, at least 18 answers are correct (checked by office staff).
4. Ask a question that is not in the handbook ("What is the canteen menu today?") and the bot says "I don't know. Please ask the office."
5. Ask for personal data ("What are my marks?") and the bot says it can't see personal data and points to the office.
6. 19 out of 20 answers appear in under 10 seconds.
7. The chat works on a phone screen (360 px wide) without side-scrolling.

## 9. Risks

| Risk | What we do about it |
| --- | --- |
| Bot gives a wrong answer and a student misses a deadline | Page number on every answer, the "I don't know" rule, and a 20-question test by office staff before launch |
| Handbook changes, bot gives old answers | One named person uploads the new PDF every semester |
| Students treat the bot as the final word | A line under every answer: "For official decisions, contact the college office." |
| PDF is scanned or has complex tables, so the bot can't read it | Test text extraction on the real PDF in week 1 |

## 10. Open Questions

1. Who will update the handbook PDF every semester?
2. Where will the bot live: the college website, or a separate link?
3. Do we need Hindi in v1, or can it wait for "Later"?
4. Who signs off on the 20 test questions: Mrs. Sharma or the Dean?
5. What is the monthly budget for AI costs?
