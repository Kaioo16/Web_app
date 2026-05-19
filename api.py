import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "segredo"

def conectar():
    conn = sqlite3.connect("app.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT UNIQUE,
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

# ---------------- CADASTRO ----------------
@app.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.json
    conn = conectar()

    senha_hash = generate_password_hash(data["senha"])

    try:
        conn.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (data["usuario"], senha_hash)
        )
        conn.commit()
        return jsonify({"status": "ok"})
    except:
        return jsonify({"status": "erro", "msg": "usuário já existe"})

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = conectar()

    user = conn.execute(
        "SELECT * FROM usuarios WHERE usuario=?",
        (data["usuario"],)
    ).fetchone()

    if user and check_password_hash(user[2], data["senha"]):
        return jsonify({"status": "ok", "user_id": user[0]})

    return jsonify({"status": "erro"})

# ---------------- TAREFAS ----------------
@app.route("/tarefas/<int:user_id>", methods=["GET"])
def listar(user_id):
    conn = conectar()

    tarefas = conn.execute(
        "SELECT * FROM tarefas WHERE user_id=?",
        (user_id,)
    ).fetchall()

    return jsonify([
        {"id": t[0], "nome": t[1]} for t in tarefas
    ])

@app.route("/tarefas", methods=["POST"])
def adicionar():
    data = request.json
    conn = conectar()

    conn.execute(
        "INSERT INTO tarefas (nome, user_id) VALUES (?, ?)",
        (data["nome"], data["user_id"])
    )
    conn.commit()

    return jsonify({"status": "ok"})

@app.route("/tarefas/<int:id>", methods=["DELETE"])
def apagar(id):
    conn = conectar()

    conn.execute(
        "DELETE FROM tarefas WHERE id=?",
        (id,)
    )
    conn.commit()

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
