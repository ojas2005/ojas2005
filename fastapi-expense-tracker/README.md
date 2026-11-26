# 💸 FastAPI Expense Tracker

A small full-stack app: a **FastAPI** backend with SQLite storage and a plain **HTML/CSS/JS** frontend that the backend serves.

## Features
- Add expenses with a title, amount, category and date
- List and delete expenses
- See the total and a per-category breakdown

## Project structure
```
fastapi-expense-tracker/
├── backend/
│   └── main.py        # FastAPI app: REST API + serves the frontend
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js         # Calls the API with fetch()
└── requirements.txt
```

## Run it
```bash
cd fastapi-expense-tracker
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
Open http://127.0.0.1:8000 for the app, or http://127.0.0.1:8000/docs for the interactive API docs.

## API
| Method | Endpoint               | Description             |
|--------|------------------------|-------------------------|
| GET    | `/api/expenses`        | List all expenses       |
| POST   | `/api/expenses`        | Create an expense       |
| DELETE | `/api/expenses/{id}`   | Delete an expense       |
| GET    | `/api/summary`         | Total + per-category    |
