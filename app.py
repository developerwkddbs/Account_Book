from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "account_v2.db"

def get_db():
    return sqlite3.connect(DB_NAME)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
    else:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

    query = "SELECT id, type, amount, memo, created_at FROM records"
    params = []

    if start_date and end_date:
        query += " WHERE date(created_at) BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    query += " ORDER BY id DESC"

    cur.execute(query, params)
    records = cur.fetchall()

    total_income = sum(r[2] for r in records if r[1] == "income")
    total_expense = sum(r[2] for r in records if r[1] == "expense")
    balance = total_income - total_expense

    conn.close()
    return render_template("index.html",
                           records=records,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance)

@app.route("/add", methods=["POST"])
def add():
    type_ = request.form.get("type")      # income / expense
    amount = request.form.get("amount")
    memo = request.form.get("memo")

    if not type_ or not amount:
        return redirect(url_for("index"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO records (type, amount, memo, created_at) VALUES (?, ?, ?, datetime('now'))",
        (type_, int(amount), memo)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:record_id>")
def delete(record_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/stats/pie")
def stats_pie():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS expense
        FROM records
    """)
    income, expense = cur.fetchone()
    conn.close()

    return jsonify({
        "labels": ["수입", "지출"],
        "data": [income or 0, expense or 0]
    })

if __name__ == "__main__":
    app.run(debug=True)
