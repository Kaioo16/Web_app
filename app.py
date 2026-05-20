from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "minha_chave_super_secreta_2026"
@app.route("/upload", methods=["POST"])
def upload():
    arquivo = request.files["file"]

    os.makedirs("uploads", exist_ok=True)

    caminho = os.path.join("uploads", arquivo.filename)
    arquivo.save(caminho)

    return "Upload feito com sucesso"

def get_db():
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    return sqlite3.connect("app.db")


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    arquivos = os.listdir("uploads") if os.path.exists("uploads") else []

    return render_template("dashboard.html", arquivos=arquivos)


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
        session["user"] = username
        return redirect(url_for("dashboard"))

    return "Login inválido"

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
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
            ("kaiote", generate_password_hash("1603"))
        )

    conn.commit()
    conn.close()

init_db()
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        senha_hash = generate_password_hash(password)

        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, senha_hash)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return render_template("register.html")
