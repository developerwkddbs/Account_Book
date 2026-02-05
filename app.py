from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "account_v2.db"

def get_db():
    return sqlite3.connect(DB_NAME)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    # 테이블 없으면 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,        -- income / expense
            amount INTEGER NOT NULL,
            memo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    if request.method == "POST":
        r_type = request.form["type"]
        amount = request.form["amount"]
        memo = request.form["memo"]

        cur.execute(
            "INSERT INTO records (type, amount, memo) VALUES (?, ?, ?)",
            (r_type, amount, memo)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    cur.execute("SELECT id, type, amount, memo, created_at FROM records ORDER BY id DESC")
    records = cur.fetchall()
    conn.close()

    return render_template("index.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
