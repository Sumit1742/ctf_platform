from flask import Flask, request, jsonify
import jwt, os, json, base64, hmac, hashlib

app = Flask(__name__)
FLAG    = os.environ.get('FLAG', 'CTF{jwt_4lg_n0n3_4nd_w34k_s3cr3t}')
SECRET  = 'password123'

with open('/app/private.pem', 'w') as f:
    f.write("""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2a2rwplBQLF29amygykEMmYz0+Kcj3bKBp29Ho3GEXB8kEm
Yo3TVZPQE9eBcMD7fJfDX6kRYh8qbm3oRuqZWzSBs3P8AHElXXmQcpFnJuMZwhs
N4KI1RSbTSUPLxMBpHg6FDiCgQnLpJvAGKmtLHRcMo5e3dLM+7jFq6KvxFpHVN
FakzYCHyBwq8RHWs4xrS0KiWBdQHQA7cLQIDAQABAoIBAC5RgZ+hBx7xHNaMpPgw
GptLfEqSuVqiUiH3mTRGMPPAe3VJfRiR4J0VPCfwEFqKakXTwCqMOVzIB7JRoFr
1wGjgFRlcMRIOXsZkbMmBhqXLDg3XZ1iXwYSiS2n36p+ABOkFhV07rSAFDSM9G
IEd8b4T1pq2Z3OfD5VqzqhEXoMJpGJXFKnbxNIQlNSl7r3KBuaSaL4HNHAJ4ne
FIc5AeJWOGMhFoGmYAijpQ2F8YtP7BJZAO6mViiXDDFLCyFRFi1YvnuMGPBkiw
O+4sJDnZGBLMTtZ5iAZ4P6aWpM9yN3e6FJ5qL6wfUCkQsI+yBGCHuIAA0ECgYEA
-----END RSA PRIVATE KEY-----""")

with open('/app/public.pem', 'w') as f:
    f.write("""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2a2rwplBQLzygykEMmYz
0+Kcj3bKBp29Ho3GEXB8kEmYo3TVZPQE9eBcMD7fJfDX6kRYh8qbm3oRuqZWzSB
s3P8AHElXXmQcpFnJuMZwhsN4KI1RSbTSUPLxMBpHg6FDiCgQnLpJvAGKmtLHRc
Mo5e3dLM+7jFq6KvxFpHVNFakzYCHyBwq8RHWs4xrS0KiWBdQHQA7cLQIDAQAB
-----END PUBLIC KEY-----""")

def decode_b64(s):
    s = s + '=' * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)

def verify_token(token):
    try:
        parts = token.split('.')
        if len(parts) != 3: return None
        header = json.loads(decode_b64(parts[0]))
        payload = json.loads(decode_b64(parts[1]))
        alg = header.get('alg', '').lower()

        if alg == 'none' or alg == '':
            return payload

        if alg == 'hs256':
            sig = base64.urlsafe_b64encode(
                hmac.new(SECRET.encode(), f'{parts[0]}.{parts[1]}'.encode(), hashlib.sha256).digest()
            ).rstrip(b'=').decode()
            if sig == parts[2]: return payload
            sig2 = base64.urlsafe_b64encode(
                hmac.new(open('/app/public.pem','rb').read(), f'{parts[0]}.{parts[1]}'.encode(), hashlib.sha256).digest()
            ).rstrip(b'=').decode()
            if sig2 == parts[2]: return payload

        return None
    except Exception:
        return None

@app.route('/')
def index():
    return '''<!DOCTYPE html><html><head><title>JWT API</title>
<style>body{background:#111;color:#eee;font-family:monospace;padding:2rem;max-width:800px;margin:0 auto}
h1{color:#38bdf8}code{background:#1e293b;padding:2px 8px;border-radius:3px;color:#00ff9d}
.ep{padding:0.6rem 1rem;background:#1e293b;border-radius:6px;margin:0.5rem 0;border-left:3px solid #38bdf8}</style></head>
<body><h1>JWT Auth API</h1>
<p>Endpoints:</p>
<div class="ep">GET <code>/api/token</code> — get a guest JWT</div>
<div class="ep">GET <code>/api/pubkey</code> — get the RS256 public key</div>
<div class="ep">GET <code>/api/admin</code> — requires admin JWT → returns flag</div>
<p style="margin-top:1.5rem;color:#64748b">Include token as: Authorization: Bearer &lt;token&gt;</p>
</body></html>'''

@app.route('/api/token')
def get_token():
    token = jwt.encode({'role': 'guest', 'user': 'player'}, SECRET, algorithm='HS256')
    return jsonify({'token': token, 'algorithm': 'HS256', 'note': 'You are a guest. Admins see the flag.'})

@app.route('/api/pubkey')
def pubkey():
    return open('/app/public.pem').read(), 200, {'Content-Type': 'text/plain'}

@app.route('/api/admin')
def admin():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({'error': 'No token provided. Use: Authorization: Bearer <token>'}), 401
    token = auth[7:]
    payload = verify_token(token)
    if payload and payload.get('role') == 'admin':
        return jsonify({'flag': FLAG, 'message': 'Welcome, admin!'})
    return jsonify({'error': 'Access denied. Admin role required.'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
