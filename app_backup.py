from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "dev"


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user[0], password):
        return redirect(url_for("dashboard"))

    return "Login inválido"

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
 from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("SELECT * FROM users WHERE username='admin'")

    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", generate_password_hash("1234"))
        )

    conn.commit()
    conn.close()

init_db()
