import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{r3fl3ct3d_xss_n0_s4n1t1z4t10n}")

INDEX = """<!DOCTYPE html>
<html>
<head>
  <title>Product Search</title>
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
    .results{background:#0d1117;border:1px solid #30363d;padding:16px;
             border-radius:6px;margin-top:12px;min-height:48px}
    .hint{background:#161b22;border-left:3px solid #d29922;padding:12px;
          color:#8b949e;font-size:.85em;margin-top:20px;border-radius:0 4px 4px 0}
    code{background:#21262d;padding:2px 6px;border-radius:4px;color:#e6edf3}
  </style>
</head>
<body>
<div class="card">
  <h1>🔍 Product Search</h1>
  <p style="color:#8b949e">Search our catalogue of fine products.</p>
  <form method="GET">
    <input type="text" name="q" placeholder="Search products..." value="{{ raw_q }}">
    <button type="submit">Search</button>
  </form>
  {% if raw_q %}
  <div class="results">
    Showing results for: {{ raw_q | safe }}<br>
    <span style="color:#8b949e">No products matched your search.</span>
  </div>
  {% endif %}
  <div class="hint">
    💡 The search term is reflected directly into the page. What could you inject?
  </div>
</div>
</body>
</html>"""

@app.route("/")
def index():
    q = request.args.get("q", "")
    return render_template_string(INDEX, raw_q=q)

@app.route("/flag")
def flag():
    # Endpoint triggered by the XSS payload
    if request.args.get("xss"):
        return f"""<pre style="background:#0d0d0d;color:#3fb950;padding:20px;font-family:monospace">
🎉 XSS triggered successfully!
Flag: {FLAG}
</pre>"""
    return "Nothing to see here.", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
