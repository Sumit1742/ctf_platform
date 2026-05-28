from flask import Flask, request, make_response, redirect, url_for
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{s3ss10n_h1j4ck1ng_1s_d4ng3r0us}')

SESSIONS = {str(i): 'guest' for i in range(1000, 1100)}
SESSIONS['1337'] = 'admin'

HTML = """<!DOCTYPE html>
<html><head><title>SecureBank Login</title>
<style>body{{background:#111;color:#eee;font-family:monospace;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}}
.box{{background:#1a1a2e;border:1px solid #333;border-radius:8px;padding:2rem;max-width:400px;width:100%}}
h1{{color:#00ff9d;margin-bottom:1rem}}input{{width:100%;background:#0d0d0d;border:1px solid #333;color:#eee;padding:8px;border-radius:4px;margin:4px 0 12px;font-family:monospace;box-sizing:border-box}}
button{{width:100%;background:#00ff9d;color:#000;border:none;padding:10px;border-radius:4px;cursor:pointer;font-weight:bold}}
.info{{margin-top:1rem;font-size:0.85rem;color:#666}}.flag{{color:#00ff9d;word-break:break-all}}</style></head>
<body><div class="box">{content}</div></body></html>"""

@app.route('/')
def index():
    session_id = request.cookies.get('session_id')
    if session_id and SESSIONS.get(session_id) == 'admin':
        content = f'<h1>Admin Panel</h1><p>Welcome, admin!</p><p class="flag">FLAG: {FLAG}</p>'
    elif session_id and session_id in SESSIONS:
        content = f'<h1>Dashboard</h1><p>Welcome, guest!</p><p class="info">Session ID: {session_id}</p><p class="info">You need admin access to see the flag.</p><a href="/logout" style="color:#f87171">Logout</a>'
    else:
        content = '<h1>SecureBank</h1><form action="/login" method="post"><input name="user" placeholder="Username"><input name="pass" type="password" placeholder="Password"><button>Login</button></form><p class="info">Login as guest/guest to start.</p>'
    return HTML.format(content=content)

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('user') == 'guest' and request.form.get('pass') == 'guest':
        resp = make_response(redirect('/'))
        import random
        sid = str(random.randint(1000, 1099))
        SESSIONS[sid] = 'guest'
        resp.set_cookie('session_id', sid)
        return resp
    return HTML.format(content='<h1>Login Failed</h1><a href="/">Back</a>')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('session_id')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
