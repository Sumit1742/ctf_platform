"""
NovaTech Solutions — Google Dorking OSINT Challenge
Place this at: challenges/osint_dorking/app.py

Players visit http://localhost:5006, find /robots.txt hints /secret.txt,
then GET /secret.txt to read the flag.
"""
from flask import Flask
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{d0rk1ng_f1nds_s3cr3ts}')

HOME_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>NovaTech Solutions – Innovative Technology</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',Arial,sans-serif;background:#f4f6f9;color:#333}
    header{background:#1a237e;color:#fff;padding:18px 40px;display:flex;align-items:center;justify-content:space-between}
    header h1{font-size:1.6rem}
    nav a{color:#90caf9;text-decoration:none;margin-left:20px;font-size:.95rem}
    .hero{background:linear-gradient(135deg,#1a237e,#283593);color:#fff;padding:80px 40px;text-align:center}
    .hero h2{font-size:2.4rem;margin-bottom:16px}
    .hero p{font-size:1.1rem;color:#c5cae9;max-width:600px;margin:0 auto}
    .cards{display:flex;gap:24px;padding:40px;max-width:960px;margin:0 auto}
    .card{background:#fff;border-radius:8px;padding:24px;flex:1;box-shadow:0 2px 8px rgba(0,0,0,.08)}
    .card h3{color:#1a237e;margin-bottom:10px}
    footer{text-align:center;padding:20px;background:#1a237e;color:#90caf9;font-size:.85rem;margin-top:40px}
  </style>
</head>
<body>
  <header>
    <h1>NovaTech Solutions</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/services">Services</a>
      <a href="/contact">Contact</a>
    </nav>
  </header>
  <div class="hero">
    <h2>Innovating Tomorrow, Today</h2>
    <p>Enterprise-grade software solutions trusted by Fortune 500 companies worldwide.</p>
  </div>
  <div class="cards">
    <div class="card"><h3>Cloud Solutions</h3><p>Scalable infrastructure for modern businesses.</p></div>
    <div class="card"><h3>Cybersecurity</h3><p>Protecting assets with industry-leading security.</p></div>
    <div class="card"><h3>AI & Analytics</h3><p>Data-driven insights for your decisions.</p></div>
  </div>
  <footer>&copy; 2024 NovaTech Solutions. All rights reserved.</footer>
</body>
</html>"""

@app.route('/')
def home():
    return HOME_HTML

@app.route('/about')
def about():
    return """<!DOCTYPE html><html><head><title>About – NovaTech</title>
<style>body{font-family:Arial,sans-serif;padding:40px;max-width:800px;margin:0 auto;background:#f4f6f9}
h1{color:#1a237e}p{line-height:1.7;margin:12px 0}a{color:#1a237e}</style></head>
<body><a href="/">← Home</a><h1>About NovaTech Solutions</h1>
<p>Founded in 2010, NovaTech Solutions is a leading provider of enterprise technology services.</p>
<p>Our 500+ engineers deliver cutting-edge solutions across cloud, AI, and cybersecurity.</p>
</body></html>"""

@app.route('/services')
def services():
    return """<!DOCTYPE html><html><head><title>Services – NovaTech</title>
<style>body{font-family:Arial,sans-serif;padding:40px;max-width:800px;margin:0 auto;background:#f4f6f9}
h1{color:#1a237e}ul{line-height:2}a{color:#1a237e}</style></head>
<body><a href="/">← Home</a><h1>Our Services</h1>
<ul><li>Cloud Infrastructure Migration</li><li>Enterprise Security Audits</li>
<li>Custom Software Development</li><li>AI / ML Integration</li><li>24/7 Managed Support</li></ul>
</body></html>"""

@app.route('/contact')
def contact():
    return """<!DOCTYPE html><html><head><title>Contact – NovaTech</title>
<style>body{font-family:Arial,sans-serif;padding:40px;max-width:600px;margin:0 auto;background:#f4f6f9}
h1{color:#1a237e}p{line-height:1.7}a{color:#1a237e}</style></head>
<body><a href="/">← Home</a><h1>Contact Us</h1>
<p>Email: info@novatech-solutions.com</p>
<p>Phone: +1 (800) 555-0192</p>
<p>Address: 1337 Innovation Drive, San Francisco, CA 94105</p>
</body></html>"""

@app.route('/robots.txt')
def robots():
    # Gives players a nudge
    return (
        "User-agent: *\n"
        "Allow: /\n\n"
        "# Internal files - please ignore\n"
        "# /secret.txt\n"
        "# /admin/\n"
        "# /backup/\n"
    ), 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        '<url><loc>http://localhost:5006/</loc></url>'
        '<url><loc>http://localhost:5006/about</loc></url>'
        '<url><loc>http://localhost:5006/services</loc></url>'
        '<url><loc>http://localhost:5006/contact</loc></url>'
        '</urlset>'
    ), 200, {'Content-Type': 'application/xml'}

@app.route('/secret.txt')
def secret():
    """The accidentally-exposed file — this is what players must find."""
    return (
        f"NovaTech Solutions — Internal Configuration Notes\n"
        f"==================================================\n"
        f"Last updated: 2024-03-15  |  Author: sysadmin@novatech-solutions.com\n\n"
        f"[IMPORTANT] Do NOT share this file externally.\n\n"
        f"Database credentials (staging):\n"
        f"  host: db-staging.novatech.internal\n"
        f"  user: ntadmin\n"
        f"  pass: Nv@St4g1ng!2024\n\n"
        f"CTF Flag (proof of access):\n"
        f"  {FLAG}\n\n"
        f"Action items:\n"
        f"  [ ] Rotate all staging credentials before Q2\n"
        f"  [ ] Remove this file from public web root  ← STILL PENDING\n"
    ), 200, {'Content-Type': 'text/plain'}

@app.route('/<path:path>')
def catch_all(path):
    return (
        "<!DOCTYPE html><html><head><title>404 – NovaTech</title>"
        "<style>body{font-family:Arial,sans-serif;text-align:center;padding:80px;background:#f4f6f9}"
        "h1{color:#c62828;font-size:4rem}a{color:#1a237e}</style></head>"
        "<body><h1>404</h1><p>Page not found.</p><a href='/'>← Back to Home</a></body></html>"
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
