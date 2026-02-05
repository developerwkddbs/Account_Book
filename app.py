from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "account_v2.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def ensure_detail_column():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE records ADD COLUMN detail TEXT")
        conn.commit()
    except:
        pass
    conn.close()


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

    query = "SELECT id, type, amount, memo, detail, created_at FROM records"
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
    detail=request.form.get("detail")

    if not type_ or not amount:
        return redirect(url_for("index"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO records (type, amount, memo, detail, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
        (type_, int(amount), memo, detail)
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

from flask import jsonify

@app.route("/stats/all_pie")
def stats_all_pie():
    conn = get_db()
    cur = conn.cursor()

    # type + memo 기준 합계
    cur.execute("""
        SELECT type, memo, SUM(amount) as total
        FROM records
        WHERE memo IS NOT NULL AND memo != ''
        GROUP BY type, memo
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    conn.close()

    labels = []
    data = []

    for t, memo, total in rows:
        prefix = "수입" if t == "income" else "지출"
        labels.append(f"{prefix}-{memo}")
        data.append(total)

    return jsonify({"labels": labels, "data": data})

if __name__ == "__main__":
    ensure_detail_column()
    app.run(debug=True)