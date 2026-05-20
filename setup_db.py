import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("app.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")

cur.execute("DELETE FROM users")

cur.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    ("admin", generate_password_hash("1234"))
)

conn.commit()
conn.close()

print("OK - banco criado")
