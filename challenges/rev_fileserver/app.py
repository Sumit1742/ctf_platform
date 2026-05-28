from flask import Flask, request, send_from_directory, abort, render_template_string
import os, hashlib, hmac, time

app = Flask(__name__)
FILES_DIR = '/app/files'

# Files are NOT listed. Each has a secret token derived from a puzzle answer.
# Players must solve the story clue to derive the token, then hit /get/<token>
# Tokens are HMAC-SHA256(secret, filename) — unguessable without solving puzzle.

_SECRET = b'nightfall_op_2024'

def make_token(filename):
    return hmac.new(_SECRET, filename.encode(), hashlib.sha256).hexdigest()[:24]

FILE_TOKENS = {
    make_token('agent_verify'):     'agent_verify',
    make_token('vault_access'):     'vault_access',
    make_token('nightfall_daemon'): 'nightfall_daemon',
    make_token('mission.pyc'):      'mission.pyc',
    make_token('nightfall_vm'):     'nightfall_vm',
}

# The landing page gives nothing away — just an investigation board
INDEX = """<!DOCTYPE html>
<html>
<head>
<title>NIGHTFALL // RECOVERED TERMINAL</title>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #060a0e;
    color: #8aad8a;
    font-family: 'Share Tech Mono', 'Courier New', monospace;
    min-height: 100vh;
    padding: 2rem;
  }
  .header {
    border-bottom: 1px solid #1a2a1a;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
  }
  .title { color: #3d7a3d; font-size: 0.75rem; letter-spacing: 6px; }
  .subtitle { color: #1a3a1a; font-size: 0.65rem; letter-spacing: 3px; margin-top: 4px; }
  .log-entry {
    padding: 0.6rem 0;
    border-bottom: 1px solid #0d1a0d;
    font-size: 0.82rem;
    line-height: 1.6;
    color: #6a9a6a;
  }
  .ts { color: #2a4a2a; margin-right: 1rem; }
  .warn { color: #7a6a2a; }
  .err  { color: #7a2a2a; }
  .info { color: #2a5a7a; }
  .prompt-area {
    margin-top: 2rem;
    background: #080e08;
    border: 1px solid #1a2a1a;
    border-radius: 4px;
    padding: 1.2rem;
  }
  .prompt-label { font-size: 0.7rem; color: #2a4a2a; letter-spacing: 2px; margin-bottom: 0.8rem; }
  .prompt-row { display: flex; gap: 0.5rem; }
  input[type=text] {
    flex: 1; background: #060a0e;
    border: 1px solid #1a2a1a; border-radius: 2px;
    padding: 8px 12px; color: #8aad8a;
    font-family: 'Share Tech Mono', monospace; font-size: 0.85rem;
    outline: none;
  }
  input:focus { border-color: #3d7a3d; }
  button {
    background: transparent; border: 1px solid #3d7a3d;
    color: #3d7a3d; padding: 8px 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem; cursor: pointer; border-radius: 2px;
    transition: all 0.15s; letter-spacing: 2px;
  }
  button:hover { background: rgba(61,122,61,0.1); }
  .result {
    margin-top: 1rem; font-size: 0.82rem; padding: 0.7rem;
    border-radius: 2px; display: none;
  }
  .result-ok  { color: #5aaa5a; background: rgba(90,170,90,0.05); border: 1px solid #1a4a1a; }
  .result-err { color: #aa5a5a; background: rgba(170,90,90,0.05); border: 1px solid #4a1a1a; }
  .fragment {
    margin-top: 2.5rem;
    background: #080e08;
    border: 1px solid #1a2a1a;
    padding: 1.2rem;
    border-radius: 4px;
  }
  .frag-title { font-size: 0.7rem; color: #2a5a7a; letter-spacing: 3px; margin-bottom: 1rem; }
  .frag-content { font-size: 0.8rem; color: #4a7a6a; line-height: 1.9; white-space: pre-wrap; }
  .redacted { background: #3a2a2a; color: #3a2a2a; padding: 0 4px; border-radius: 2px; }
  .cursor { animation: blink 1s step-end infinite; }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
  .download-link {
    display: inline-block; margin-top: 1rem;
    color: #5aaa5a; text-decoration: none;
    border: 1px solid #1a4a1a; padding: 6px 16px;
    border-radius: 2px; font-size: 0.8rem; letter-spacing: 1px;
  }
  .download-link:hover { background: rgba(90,170,90,0.08); }
</style>
</head>
<body>

<div class="header">
  <div class="title">// NIGHTFALL OPERATION — RECOVERED SYSTEM TERMINAL</div>
  <div class="subtitle">CIPHER CLUB INTELLIGENCE DIVISION — CASE FILE #0x41</div>
</div>

<div class="log-entry">
  <span class="ts">[2024-01-15 03:42:11]</span>
  <span class="warn">WARN</span> &nbsp; Unauthorised access detected on NIGHTFALL internal network.
</div>
<div class="log-entry">
  <span class="ts">[2024-01-15 03:42:19]</span>
  <span class="err">CRIT</span> &nbsp; Agent ECHO failed authentication — 3 attempts.
</div>
<div class="log-entry">
  <span class="ts">[2024-01-15 03:42:31]</span>
  <span class="info">INFO</span> &nbsp; Payload artifacts staged for exfiltration: <span class="redacted">XXXXXXXXXX</span>
</div>
<div class="log-entry">
  <span class="ts">[2024-01-15 03:43:07]</span>
  <span class="warn">WARN</span> &nbsp; Secure drop channel active. Token-gated. No directory access.
</div>
<div class="log-entry">
  <span class="ts">[2024-01-15 03:44:55]</span>
  <span class="err">CRIT</span> &nbsp; NIGHTFALL vault breach imminent. Evidence recovery in progress.
</div>
<div class="log-entry">
  <span class="ts">[2024-01-15 04:01:00]</span>
  <span class="info">INFO</span> &nbsp; System frozen. Awaiting authorised retrieval. <span class="cursor">█</span>
</div>

<div class="fragment">
  <div class="frag-title">// RECOVERED FRAGMENT — PARTIAL DECRYPT</div>
  <div class="frag-content">FROM: handler@nightfall.int
TO:   field-ops
SUBJ: artifact retrieval protocol

All mission artifacts are staged at this terminal.
Access is token-gated. Tokens are NOT stored here.

Retrieval path: /get/&lt;TOKEN&gt;

Each artifact token is derived from the artifact name using
the operation HMAC key. The key was transmitted via dead-drop
in the mission briefing documents.

If you have recovered the mission briefing, you already have
what you need. If not — start over from the beginning.

  -- handler</div>
</div>

<div class="prompt-area">
  <div class="prompt-label">// TOKEN RETRIEVAL — ENTER ARTIFACT ACCESS TOKEN</div>
  <div class="prompt-row">
    <input type="text" id="token-input" placeholder="enter token..." spellcheck="false" autocomplete="off">
    <button onclick="retrieve()">RETRIEVE</button>
  </div>
  <div class="result" id="result-box"></div>
</div>

<script>
function retrieve() {
  const token = document.getElementById('token-input').value.trim();
  if (!token) return;
  const box = document.getElementById('result-box');
  box.style.display = 'none';
  fetch('/get/' + token)
    .then(r => {
      if (r.ok) {
        return r.blob().then(blob => {
          const cd = r.headers.get('Content-Disposition') || '';
          const m  = cd.match(/filename="?([^"]+)"?/);
          const fn = m ? m[1] : 'artifact';
          const url = URL.createObjectURL(blob);
          box.className = 'result result-ok';
          box.innerHTML = '[+] artifact located: ' + fn +
            '<br><a class="download-link" href="' + url + '" download="' + fn + '">↓ DOWNLOAD ' + fn.toUpperCase() + '</a>';
          box.style.display = 'block';
        });
      } else {
        box.className = 'result result-err';
        box.textContent = '[-] invalid token — no artifact found.';
        box.style.display = 'block';
      }
    })
    .catch(() => {
      box.className = 'result result-err';
      box.textContent = '[-] connection error.';
      box.style.display = 'block';
    });
}
document.getElementById('token-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') retrieve();
});
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(INDEX)

@app.route('/get/<token>')
def get_file(token):
    filename = FILE_TOKENS.get(token)
    if not filename:
        # Timing-safe rejection — don't leak token validity timing
        time.sleep(0.1)
        abort(404)
    return send_from_directory(FILES_DIR, filename, as_attachment=True)

# No /files/, no /list/, no /download/ — nothing else exposed
@app.errorhandler(404)
def not_found(e):
    return '[-] not found.', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5016, debug=False)
