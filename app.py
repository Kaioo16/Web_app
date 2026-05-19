import sqlite3
from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = "segredo"

def db():
    conn = sqlite3.connect("app.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT,
            senha TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            user_id INTEGER
        )
    """)
    return conn

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    conn = db()

    if request.method == "POST":
        u = request.form.get("usuario")
        s = request.form.get("senha")

        user = conn.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
            (u, s)
        ).fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect("/tarefas")

        return "Login inválido"

    return """
    <div style="text-align:center;font-family:Arial">
        <h2>Login</h2>
        <form method="POST">
            <input name="usuario" placeholder="Usuário"><br><br>
            <input name="senha" type="password" placeholder="Senha"><br><br>
            <button>Entrar</button>
        </form>
    </div>
    """

# TAREFAS
@app.route("/tarefas", methods=["GET", "POST"])
def tarefas():
    if "user_id" not in session:
        return redirect("/")

    conn = db()
    uid = session["user_id"]

    if request.method == "POST" and "nova" in request.form:
        conn.execute(
            "INSERT INTO tarefas (nome, user_id) VALUES (?, ?)",
            (request.form["nova"], uid)
        )
        conn.commit()
        return redirect("/tarefas")

    if request.method == "POST" and "apagar" in request.form:
        conn.execute(
            "DELETE FROM tarefas WHERE id=? AND user_id=?",
            (request.form["apagar"], uid)
        )
        conn.commit()
        return redirect("/tarefas")

    tarefas = conn.execute(
        "SELECT * FROM tarefas WHERE user_id=?",
        (uid,)
    ).fetchall()

    html = """
    <html>
    <head>
    <style>
        body {
            font-family: Arial;
            background: #111;
            color: white;
            margin: 0;
        }

        .top {
            background: #222;
            padding: 15px;
            text-align: center;
        }

        .container {
            padding: 15px;
        }

        .card {
            background: #1e1e1e;
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
        }

        input {
            padding: 10px;
            width: 70%;
        }

        button {
            padding: 10px;
            background: #4CAF50;
            border: none;
            color: white;
        }

        .delete {
            background: red;
        }
    </style>
    </head>
    <body>

    <div class="top">
        <h2>Minhas Tarefas</h2>
    </div>

    <div class="container">

        <form method="POST">
            <input name="nova" placeholder="Nova tarefa">
            <button>+</button>
        </form>

        <br>
    """

    for t in tarefas:
        html += f"""
        <div class="card">
            <span>{t[1]}</span>
            <form method="POST">
                <button class="delete" name="apagar" value="{t[0]}">X</button>
            </form>
        </div>
        """

    html += """
    </div>

    </body>
    </html>
    """

    return html

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
