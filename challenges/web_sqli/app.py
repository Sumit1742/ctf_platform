from flask import Flask, request, render_template_string
import sqlite3, os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{sql_1nj3ct10n_f0r_th3_w1n}')

PAGE = """<!DOCTYPE html>
<html>
<head>
<title>Admin Panel</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0d1117; color: #e6edf3; font-family: monospace; display: flex;
         justify-content: center; align-items: center; min-height: 100vh; }
  .box { background: #161b22; border: 1px solid #30363d; border-radius: 8px;
         padding: 2.5rem; width: 380px; }
  h2 { color: #58a6ff; font-size: 1.1rem; letter-spacing: 2px; margin-bottom: 1.5rem; }
  label { display: block; font-size: 0.75rem; color: #8b949e; letter-spacing: 1px;
          text-transform: uppercase; margin-bottom: 0.3rem; }
  input { width: 100%; background: #0d1117; border: 1px solid #30363d; border-radius: 4px;
          padding: 8px 12px; color: #e6edf3; font-family: monospace; font-size: 0.9rem;
          outline: none; margin-bottom: 1rem; }
  input:focus { border-color: #58a6ff; }
  button { width: 100%; background: #238636; border: none; border-radius: 4px;
           color: white; padding: 10px; font-family: monospace; font-size: 0.9rem;
           cursor: pointer; letter-spacing: 1px; }
  button:hover { background: #2ea043; }
  .error { color: #f85149; font-size: 0.85rem; margin-top: 1rem; }
  .flag { color: #3fb950; font-size: 0.9rem; margin-top: 1rem; background: #0d2d17;
          border: 1px solid #2ea043; padding: 1rem; border-radius: 4px; word-break: break-all; }
  .hint { color: #8b949e; font-size: 0.75rem; margin-top: 1.5rem; border-top: 1px solid #21262d;
          padding-top: 1rem; }
</style>
</head>
<body>
<div class="box">
  <h2>// ADMIN LOGIN</h2>
  <form method="POST">
    <label>Username</label>
    <input name="username" autocomplete="off" spellcheck="false">
    <label>Password</label>
    <input name="password" type="password">
    <button type="submit">LOGIN →</button>
  </form>
  {% if error %}<div class="error">✗ {{ error }}</div>{% endif %}
  {% if flag %}<div class="flag">✓ Welcome, admin!<br><br>{{ flag }}</div>{% endif %}
  <div class="hint">challenge: login bypass &nbsp;·&nbsp; find the vulnerability</div>
</div>
</body>
</html>"""


def init_db():
    conn = sqlite3.connect('/tmp/ctf.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )""")
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'Tr0ub4dor&3')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'guest', 'guest123')")
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    error = flag = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            conn = sqlite3.connect('/tmp/ctf.db')
            # INTENTIONALLY VULNERABLE — SQL INJECTION CHALLENGE
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            user = conn.execute(query).fetchone()
            conn.close()
            if user:
                flag = FLAG
            else:
                error = "Invalid credentials."
        except Exception as e:
            error = f"DB Error: {e}"
    return render_template_string(PAGE, error=error, flag=flag)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
