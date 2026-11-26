"""Expense Tracker - FastAPI backend with SQLite storage."""
import sqlite3
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "expenses.db"
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(title="Expense Tracker API", version="1.0.0")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


with get_db() as conn:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            spent_on TEXT NOT NULL
        )"""
    )


class ExpenseIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field("Other", max_length=30)
    spent_on: date = Field(default_factory=date.today)


class Expense(ExpenseIn):
    id: int


@app.get("/api/expenses", response_model=list[Expense])
def list_expenses():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM expenses ORDER BY spent_on DESC, id DESC").fetchall()
    return [dict(r) for r in rows]


@app.post("/api/expenses", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseIn):
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO expenses (title, amount, category, spent_on) VALUES (?, ?, ?, ?)",
            (expense.title, expense.amount, expense.category, expense.spent_on.isoformat()),
        )
    return {"id": cur.lastrowid, **expense.model_dump()}


@app.delete("/api/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    with get_db() as conn:
        cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Expense not found")


@app.get("/api/summary")
def summary():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT category, ROUND(SUM(amount), 2) AS total FROM expenses GROUP BY category ORDER BY total DESC"
        ).fetchall()
    by_category = {r["category"]: r["total"] for r in rows}
    return {"total": round(sum(by_category.values()), 2), "by_category": by_category}


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(FRONTEND_DIR / "index.html")
