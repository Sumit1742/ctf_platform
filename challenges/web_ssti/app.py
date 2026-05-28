import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{sst1_jinja2_rce_via_mro_chain}")
os.environ["FLAG"] = FLAG   # also reachable via config / environ in SSTI

# Weak blacklist — bypassable with attr() filter or string concatenation
BLACKLIST = ["__class__", "subprocess", "os.system", "exec(", "eval(", "import"]

INDEX = """<!DOCTYPE html>
<html>
<head>
  <title>Greeting Generator</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0d0d0d;color:#c9d1d9;font-family:monospace;
         display:flex;justify-content:center;align-items:center;min-height:100vh}
    .card{background:#161b22;border:1px solid #30363d;border-radius:10px;
          padding:40px;max-width:560px;width:100%}
    h1{color:#58a6ff;margin-bottom:8px}
    form{display:flex;gap:8px;margin:20px 0}
    input{flex:1;background:#21262d;border:1px solid #30363d;color:#e6edf3;
          padding:10px;border-radius:6px;font-family:monospace}
    button{background:#238636;color:#fff;border:none;padding:10px 20px;
           border-radius:6px;cursor:pointer;font-family:monospace}
    .output{background:#0d1117;border:1px solid #30363d;padding:16px;
            border-radius:6px;margin-top:12px}
    .error{border-color:#da3633;color:#ff7b72}
    .hint{background:#161b22;border-left:3px solid #bc8cff;padding:12px;
          color:#8b949e;font-size:.85em;margin-top:20px;border-radius:0 4px 4px 0}
    code{background:#21262d;padding:2px 6px;border-radius:4px;color:#e6edf3}
    .blocked{border-color:#d29922;color:#e3b341}
  </style>
</head>
<body>
<div class="card">
  <h1>👋 Greeting Generator</h1>
  <p style="color:#8b949e">Enter your name for a personalised greeting.</p>
  <form method="GET">
    <input type="text" name="name" placeholder="Your name..." value="{{ raw_name }}">
    <button type="submit">Generate</button>
  </form>

  {% if blocked %}
    <div class="output blocked">🚫 Blocked keyword detected in input.</div>
  {% elif output %}
    <div class="output">{{ output }}</div>
  {% endif %}

  <div class="hint">
    💡 Your name is rendered <em>directly</em> inside a Jinja2 template string.
    Start with <code>{{"{{"}}7*7{{"}}"}}</code> — if you see <strong>49</strong>, SSTI is confirmed.
    The flag lives in the environment variable <code>FLAG</code>.
  </div>
</div>
</body>
</html>"""

@app.route("/")
def index():
    name = request.args.get("name", "")
    raw_name = name
    output = blocked = ""

    if name:
        if any(b in name for b in BLACKLIST):
            blocked = True
        else:
            try:
                template = f"Hello, <strong>{name}</strong>! 🎉"
                output = render_template_string(template)
            except Exception as e:
                output = f'<span class="error">Template error: {e}</span>'

    return render_template_string(INDEX, raw_name=raw_name, output=output, blocked=blocked)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
