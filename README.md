# IPL Prediction App

This is a small, mobile-friendly web app for an IPL prediction game built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Jinja2** templates.

## Features

- Match list and prediction pages
- Pari-mutuel betting pool with live odds
- Bankroll management (starts at 20,000; bets between 200 and 2,000)
- Leaderboard based on bankroll
- Bet history for each player

## Tech Stack

- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Jinja2 templates

## Running the app

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the FastAPI app with uvicorn:

```bash
uvicorn app.main:app --reload
```

4. Open `http://127.0.0.1:8000` in your browser.

## Development notes

- The database is a local SQLite file stored in the project root.
- Users are created on first login and given an initial bankroll.
- All pages are server-rendered with Jinja2 and designed for mobile-friendly use.

