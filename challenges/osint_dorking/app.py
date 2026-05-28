"""
OSINT Challenge: Google Dorking
A fake company site that has accidentally exposed a .txt file at /secret.txt
Players must use: site:novatech-solutions-ctf.local filetype:txt  (or just find /secret.txt)
"""
from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{d0rk1ng_f1nds_s3cr3ts}')


# ── Static HTML pages (the "company website") ─────────────────────────────
HOME_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>NovaTech Solutions – Innovative Technology</title>
  <meta name="robots" content="index, follow">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; color: #333; }
    header { background: #1a237e; color: #fff; padding: 18px 40px; display: flex; align-items: center; justify-content: space-between; }
    header h1 { font-size: 1.6rem; }
    nav a { color: #90caf9; text-decoration: none; margin-left: 20px; font-size: 0.95rem; }
    .hero { background: linear-gradient(135deg, #1a237e, #283593); color: #fff; padding: 80px 40px; text-align: center; }
    .hero h2 { font-size: 2.4rem; margin-bottom: 16px; }
    .hero p  { font-size: 1.1rem; color: #c5cae9; max-width: 600px; margin: 0 auto; }
    .cards   { display: flex; gap: 24px; padding: 40px; max-width: 960px; margin: 0 auto; }
    .card    { background: #fff; border-radius: 8px; padding: 24px; flex: 1; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
    .card h3 { color: #1a237e; margin-bottom: 10px; }
    footer   { text-align: center; padding: 20px; background: #1a237e; color: #90caf9; font-size: 0.85rem; margin-top: 40px; }
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
    <div class="card">
      <h3>Cloud Solutions</h3>
      <p>Scalable infrastructure designed for modern businesses.</p>
    </div>
    <div class="card">
      <h3>Cybersecurity</h3>
      <p>Protecting your assets with industry-leading security practices.</p>
    </div>
    <div class="card">
      <h3>AI & Analytics</h3>
      <p>Data-driven insights to power your business decisions.</p>
    </div>
  </div>
  <footer>&copy; 2024 NovaTech Solutions. All rights reserved.</footer>
</body>
</html>"""

ABOUT_HTML = """<!DOCTYPE html>
<html>
<head><title>About – NovaTech Solutions</title>
<style>body{font-family:Arial,sans-serif;padding:40px;max-width:800px;margin:0 auto;background:#f4f6f9}
h1{color:#1a237e}p{line-height:1.7;margin:12px 0}
a{color:#1a237e}</style></head>
<body>
<a href="/">← Home</a>
<h1>About NovaTech Solutions</h1>
<p>Founded in 2010, NovaTech Solutions is a leading provider of enterprise technology services.</p>
<p>Our team of 500+ engineers delivers cutting-edge solutions across cloud, AI, and cybersecurity domains.</p>
<p>We are committed to innovation, integrity, and customer success.</p>
</body></html>"""

SERVICES_HTML = """<!DOCTYPE html>
<html>
<head><title>Services – NovaTech Solutions</title>
<style>body{font-family:Arial,sans-serif;padding:40px;max-width:800px;margin:0 auto;background:#f4f6f9}
h1{color:#1a237e}ul{line-height:2}a{color:#1a237e}</style></head>
<body>
<a href="/">← Home</a>
<h1>Our Services</h1>
<ul>
  <li>Cloud Infrastructure Migration</li>
  <li>Enterprise Security Audits</li>
  <li>Custom Software Development</li>
  <li>AI / ML Integration</li>
  <li>24/7 Managed Support</li>
</ul>
</body></html>"""

CONTACT_HTML = """<!DOCTYPE html>
<html>
<head><title>Contact – NovaTech Solutions</title>
<style>body{font-family:Arial,sans-serif;padding:40px;max-width:600px;margin:0 auto;background:#f4f6f9}
h1{color:#1a237e}p{line-height:1.7}a{color:#1a237e}</style></head>
<body>
<a href="/">← Home</a>
<h1>Contact Us</h1>
<p>Email: info@novatech-solutions.com</p>
<p>Phone: +1 (800) 555-0192</p>
<p>Address: 1337 Innovation Drive, San Francisco, CA 94105</p>
</body></html>"""

# ── The accidentally-exposed secret file ──────────────────────────────────
SECRET_TXT = f"""NovaTech Solutions — Internal Configuration Notes
==================================================
Last updated: 2024-03-15  |  Author: sysadmin@novatech-solutions.com

[IMPORTANT] Do NOT share this file externally.

Database credentials (staging):
  host: db-staging.novatech.internal
  user: ntadmin
  pass: Nv@St4g1ng!2024

API keys (deprecated — rotate ASAP):
  stripe_secret: sk_live_XXXX_REDACTED
  sendgrid_key : SG.XXXXXXXXX_REDACTED

CTF Flag (proof of access):
  {FLAG}

Action items:
  [ ] Rotate all staging credentials before Q2
  [ ] Migrate DB to new cluster
  [ ] Remove this file from public web root ← STILL PENDING
"""

ROBOTS_TXT = """User-agent: *
Allow: /

# Internal files - please ignore
# /secret.txt
# /admin/
# /backup/
"""

SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>http://localhost:5006/</loc></url>
  <url><loc>http://localhost:5006/about</loc></url>
  <url><loc>http://localhost:5006/services</loc></url>
  <url><loc>http://localhost:5006/contact</loc></url>
</urlset>"""


@app.route('/')
def home():
    return HOME_HTML

@app.route('/about')
def about():
    return ABOUT_HTML

@app.route('/services')
def services():
    return SERVICES_HTML

@app.route('/contact')
def contact():
    return CONTACT_HTML

@app.route('/robots.txt')
def robots():
    return ROBOTS_TXT, 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    return SITEMAP_XML, 200, {'Content-Type': 'application/xml'}

@app.route('/secret.txt')
def secret():
    """The accidentally-exposed file players must find via Google Dorking."""
    return SECRET_TXT, 200, {'Content-Type': 'text/plain'}

@app.route('/<path:path>')
def catch_all(path):
    return f"""<!DOCTYPE html>
<html><head><title>404 – NovaTech Solutions</title>
<style>body{{font-family:Arial,sans-serif;text-align:center;padding:80px;background:#f4f6f9}}
h1{{color:#c62828;font-size:4rem}}p{{color:#555}}a{{color:#1a237e}}</style></head>
<body><h1>404</h1><p>Page not found.</p><a href="/">← Back to Home</a></body></html>""", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
