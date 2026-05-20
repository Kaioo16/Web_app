from flask import Flask, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "chave_secreta"

# ---------------- BANCO ----------------

def init_db():
    conn = sqlite3.connect("app.db")
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

init_db()

# ---------------- ROTAS ----------------

@app.route("/")
def home():
    return "Servidor funcionando ✔"

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = generate_password_hash(request.form["password"])

    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    return "Usuário criado ✔"

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):
        session["user"] = username
        return redirect(url_for("dashboard"))

    return "Login inválido ❌"

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"Bem-vindo {session['user']} ✔"
    return "Não logado ❌"

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
