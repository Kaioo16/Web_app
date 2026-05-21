from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "chave_secreta"

# --- BANCO ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- HOME ---
@app.route("/")
def index():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# --- DASHBOARD ---
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

# --- LOGIN ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, password)
        )
        result = c.fetchone()
        conn.close()

        if result:
            session["user"] = user
            return render_template("login.html")
        else:
            return "Login inválido"

    return """
    <form method="post">
        <input name="username" placeholder="Usuário">
        <input name="password" type="password" placeholder="Senha">
        <button type="submit">Entrar</button>
    </form>
    """

# --- LOGOUT ---
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# --- REGISTER ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user, password)
        )
        conn.commit()
        conn.close()

        return render_template("register.html")

    return """
    <form method="post">
        <input name="username" placeholder="Novo usuário">
        <input name="password" type="password" placeholder="Senha">
        <button type="submit">Cadastrar</button>
    </form>
    """

# --- RUN ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
