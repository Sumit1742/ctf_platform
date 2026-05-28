"""
Forensics Challenge File Server
Serves all downloadable challenge files on port 5011.
"""
from flask import Flask, send_from_directory, render_template_string, abort
import os

app = Flask(__name__)

FILES_DIR = os.path.join(os.path.dirname(__file__), "challenge_files")

ALLOWED_FILES = {
    "secret.txt",
    "photo.jpg",
    "sunset.png",
    "capture.pcap",
    "secret.zip",
}

INDEX_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Forensics Challenge Files</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #e6edf3; font-family: monospace;
           display: flex; justify-content: center; padding: 3rem 1rem; }
    .container { width: 100%; max-width: 640px; }
    h1 { color: #58a6ff; font-size: 1.2rem; letter-spacing: 2px;
         margin-bottom: 0.4rem; }
    p  { color: #8b949e; font-size: 0.8rem; margin-bottom: 2rem; }
    .file { background: #161b22; border: 1px solid #30363d; border-radius: 6px;
            padding: 1rem 1.2rem; margin-bottom: 0.75rem;
            display: flex; justify-content: space-between; align-items: center; }
    .file-name { color: #3fb950; font-size: 0.95rem; }
    .file-desc { color: #8b949e; font-size: 0.75rem; margin-top: 0.2rem; }
    a.dl { background: #238636; color: white; text-decoration: none;
           padding: 6px 14px; border-radius: 4px; font-size: 0.8rem;
           letter-spacing: 1px; white-space: nowrap; }
    a.dl:hover { background: #2ea043; }
  </style>
</head>
<body>
<div class="container">
  <h1>[ FORENSICS ] Challenge Files</h1>
  <p>Download the file for your challenge below.</p>
  {% for f in files %}
  <div class="file">
    <div>
      <div class="file-name">{{ f.name }}</div>
      <div class="file-desc">{{ f.desc }}</div>
    </div>
    <a class="dl" href="/{{ f.name }}">Download</a>
  </div>
  {% endfor %}
</div>
</body>
</html>"""

FILE_DESCS = {
    "secret.txt":   "Challenge: Not What It Seems — magic bytes",
    "photo.jpg":    "Challenge: Metadata Leak — EXIF data",
    "sunset.png":   "Challenge: Hidden in Plain Sight — steganography",
    "capture.pcap": "Challenge: Packet Detective — network analysis",
    "secret.zip":   "Challenge: Locked Archive — password cracking",
}

@app.route("/")
def index():
    files = [
        {"name": name, "desc": FILE_DESCS.get(name, "")}
        for name in sorted(ALLOWED_FILES)
        if os.path.exists(os.path.join(FILES_DIR, name))
    ]
    return render_template_string(INDEX_HTML, files=files)

@app.route("/<filename>")
def serve_file(filename):
    if filename not in ALLOWED_FILES:
        abort(404)
    return send_from_directory(FILES_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
