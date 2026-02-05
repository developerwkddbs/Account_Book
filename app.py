from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app=Flask(__name__)
DB_Name="account.db"

def get_db():
    return sqlite3.connect(DB_Name)

@app.route("/",methods=["GET","POST"])
def index():
    conn=get_db()
    cur=conn.cursor()

    #If no TABLE, CREATE TABLE
    cur.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NO NULL,      -- income / expense
                ammount INTEGER NOT NULL,
                memo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    if request.method == "POST":
        r_type=request.form["type"]
        amount=request.form["amount"]
        memo=request.form["memo"]

        cur.execute(
            "INSERT INTO records (type, amount, memo) VALUES (?,?,?)",
            (r_type,amount,memo)
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