"""
OSINT Challenge: Image Geolocation
Serves suspicious.jpg at /image
Players must extract GPS EXIF metadata and identify the location.
Flag: CTF{1nd14_g4t3_n3w_d3lh1}
"""
from flask import Flask, send_file, jsonify
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{1nd14_g4t3_n3w_d3lh1}')
IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'suspicious.jpg')

INDEX_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Evidence Locker – OSINT Challenge</title>
  <style>
    body{background:#111;color:#eee;font-family:monospace;padding:2rem;max-width:720px;margin:0 auto}
    h1{color:#f59e0b}code{background:#1e293b;padding:2px 8px;border-radius:3px;color:#34d399}
    .ep{padding:.6rem 1rem;background:#1e293b;border-radius:6px;margin:.5rem 0;border-left:3px solid #f59e0b}
    .hint{border-left-color:#60a5fa}
  </style>
</head>
<body>
  <h1>🔍 Evidence Locker</h1>
  <p>A suspect posted this image online before going dark.</p>
  <p style="margin:.8rem 0">Download and analyse it — find where it was taken.</p>

  <div class="ep">GET <code>/image</code> — download the suspect image</div>

  <div class="ep hint">
    <strong>Your mission:</strong><br>
    1. Download the image<br>
    2. Identify the exact location (city &amp; landmark)<br>
    3. Submit the flag as: <code>CTF{landmark_city}</code> in lowercase with underscores<br>
    Example: <code>CTF{eiffel_tower_paris}</code>
  </div>

  <p style="margin-top:1.5rem;color:#64748b">
    Tools: <code>exiftool suspicious.jpg</code> or any EXIF viewer
  </p>
</body>
</html>"""

@app.route('/')
def index():
    return INDEX_HTML

@app.route('/image')
def serve_image():
    return send_file(IMAGE_PATH, mimetype='image/jpeg',
                     as_attachment=True, download_name='suspicious.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
