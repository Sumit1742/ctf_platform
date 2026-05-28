from flask import Flask, request, abort
import os, urllib.parse

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{p4th_tr4v3rs4l_0ut_0f_b0unds}')
BASE_DIR = '/app/files'
os.makedirs(BASE_DIR, exist_ok=True)
with open(os.path.join(BASE_DIR, 'report.pdf.txt'), 'w') as f:
    f.write('This is the annual report.')
with open('/flag.txt', 'w') as f:
    f.write(FLAG)

HTML = """<!DOCTYPE html><html><head><title>FileServer</title>
<style>body{{background:#111;color:#eee;font-family:monospace;padding:2rem;max-width:800px;margin:0 auto}}
h1{{color:#38bdf8}}code{{background:#1e293b;padding:2px 6px;border-radius:3px;color:#00ff9d}}
.file{{padding:0.5rem;border:1px solid #333;border-radius:4px;margin:0.5rem 0;display:flex;justify-content:space-between}}
a{{color:#38bdf8}}</style></head>
<body><h1>FileServer v2.0</h1>
<p>Available files:</p>
<div class="file"><span>report.pdf</span><a href="/download?file=report.pdf">Download</a></div>
<p style="margin-top:2rem;color:#64748b">API: <code>GET /download?file=&lt;filename&gt;</code></p>
</body></html>"""

def sanitize(path):
    decoded = urllib.parse.unquote(path)
    decoded = decoded.replace('../', '').replace('..\\', '')
    if decoded.startswith('/'):
        decoded = decoded[1:]
    return decoded

@app.route('/')
def index():
    return HTML

@app.route('/download')
def download():
    filename = request.args.get('file', '')
    if not filename:
        abort(400)
    clean = sanitize(filename)
    full_path = os.path.join(BASE_DIR, clean)
    full_path = os.path.normpath(full_path)
    try:
        with open(full_path, 'r') as f:
            content = f.read()
        return f'<pre style="background:#111;color:#00ff9d;padding:1rem">{content}</pre>'
    except FileNotFoundError:
        return f'<pre style="color:#f87171">File not found: {full_path}</pre>', 404
    except Exception as e:
        return f'<pre style="color:#f87171">Error: {e}</pre>', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
