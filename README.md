# Course Lab Submission Tracker

Manufacturing Practice project (Summer 2026) — a REST API that helps
teachers track student lab submissions, grades, and feedback in one
place, replacing manual spreadsheet/email tracking.

## Problem

Teachers currently track lab submissions using spreadsheets, email, and
chat messages. This makes it hard to see submission status at a glance,
and scatters grades and feedback across multiple channels.

## Users

- **Teacher**: creates courses and labs, reviews submissions, assigns
  grades and feedback.
- **Student**: submits lab work (a file link), views status and feedback.

## Tech Stack

- **Backend**: Python + FastAPI
- **Database**: SQLite, accessed via SQLAlchemy ORM
- **API docs**: auto-generated interactive docs (Swagger UI) via FastAPI
- **Version control**: Git / GitHub

## Data Model

- **Course** — a course, identified by a unique code (e.g. `SE201`).
- **Lab** — an assignment belonging to a course, with a title and deadline.
- **Submission** — a student's submission for a lab: a file/link, status,
  grade, and feedback. Linked to its lab via a foreign key
  (`labs.id`), with SQLite foreign key enforcement enabled so a
  submission cannot reference a lab that doesn't exist.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check / welcome message |
| POST | `/courses` | Create a course |
| GET | `/courses` | List all courses |
| POST | `/labs` | Create a lab (requires a valid `course_id`) |
| GET | `/labs` | List all labs |
| POST | `/submissions` | Create a submission (requires a valid `lab_id`) |
| GET | `/submissions` | List all submissions |
| PATCH | `/submissions/{id}/grade` | Grade a submission (grade + feedback) |

Interactive API docs (Swagger UI) are available at `/docs` once the
server is running.

## Setup / Run Instructions

### Prerequisites
- Python 3.10+ installed

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ASspegic/lab-tracker.git
cd lab-tracker

# 2. Install dependencies
pip install fastapi uvicorn sqlalchemy

# 3. Run the development server
uvicorn main:app --reload
```

Then open:
- `http://127.0.0.1:8000/` — welcome message
- `http://127.0.0.1:8000/docs` — interactive API documentation (Swagger UI)

The database file (`lab_tracker.db`) is created automatically on first
run — no manual setup required.

## Project Structure

```
lab-tracker/
├── main.py         # FastAPI app: routes for courses, labs, submissions
├── models.py       # SQLAlchemy models: Course, Lab, Submission
├── database.py     # Database engine/session setup, foreign key enforcement
└── README.md
```

## Status

🚧 In progress — Week 2 of Manufacturing Practice.

## Roadmap

- [x] Data models: Course, Lab, Submission (with foreign keys)
- [x] REST API: create/list for courses, labs; create/list/grade for submissions
- [x] Foreign key enforcement + clean error handling (400 instead of 500)
- [ ] Basic frontend (HTML/CSS/JS)
- [ ] Automated tests
- [ ] Docker setup
- [ ] Deployed demo link
