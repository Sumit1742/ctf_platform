# HackArena CTF Platform

Individual-only CTF platform built with Django, Python, and Docker.

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Cache / Queue**: Redis 7
- **Async tasks**: Celery
- **Live scoreboard**: Django Channels (WebSockets)
- **Server**: Gunicorn + Nginx
- **Containers**: Docker Compose

---

## Quick Start

### 1. Clone and configure

```bash
git clone <your-repo>
cd ctf_platform
cp .env.example .env   # edit as needed
```

### 2. Build and start all services

```bash
docker compose up --build -d
```

### 3. Run migrations

```bash
docker compose exec web python ctf/manage.py migrate
```

### 4. Create a superuser (admin)

```bash
docker compose exec web python ctf/manage.py createsuperuser
```

### 5. Seed the 5 challenges

```bash
docker compose exec web python ctf/manage.py seed_challenges
```

### 6. Generate challenge files (OSINT image + stego PNG)

```bash
pip install Pillow piexif
python scripts/create_challenge_files.py
# Then upload challenge_files/*.jpg and *.png via /admin/
```

### 7. Attach files via Admin

- Go to `http://localhost/admin/`
- Open each challenge → Add files → Save

### 8. Open the platform

`http://localhost/`

---

## Project Structure

```
ctf_platform/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── nginx/
│   └── nginx.conf
├── ctf/
│   ├── settings/base.py          # all config lives here
│   ├── urls.py
│   ├── asgi.py                   # WebSocket routing
│   ├── celery.py
│   ├── context_processors.py
│   ├── apps/
│   │   ├── accounts/             # Player model, auth, profiles
│   │   ├── challenges/           # Challenge model, flag submission
│   │   ├── submissions/          # Submission log
│   │   └── scoreboard/           # Live scoreboard (WS + REST)
│   ├── static/
│   │   ├── css/main.css
│   │   └── js/main.js
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── accounts/
│       ├── challenges/
│       └── scoreboard/
├── challenges/
│   ├── web_sqli/                 # Challenge 2: SQLi Flask app
│   │   ├── app.py
│   │   └── Dockerfile
│   └── pwn_bof/                  # Challenge 5: Buffer overflow
│       ├── vuln.c
│       ├── Makefile
│       └── Dockerfile
└── scripts/
    ├── create_challenge_files.py  # Generates OSINT + stego images
    ├── exploit_bof.py             # Solution: pwn challenge
    └── decode_lsb.py              # Solution: forensics challenge
```

---

## The 5 Challenges

| # | Title                    | Category   | Points | Difficulty |
|---|--------------------------|------------|--------|------------|
| 1 | Caesar's Last Secret     | Crypto     | 100    | Easy       |
| 2 | Login Bypass             | Web        | 200    | Medium     |
| 3 | Find the Whistleblower   | OSINT      | 250    | Medium     |
| 4 | Hidden in Plain Sight    | Forensics  | 300    | Medium     |
| 5 | Stack Smash 101          | Pwn/Binary | 500    | Hard       |

**Total points: 1350**

---

## Challenge Flags

| Challenge              | Flag                               |
|------------------------|------------------------------------|
| Caesar's Last Secret   | `CTF{caesar_cipher_is_too_old}`    |
| Login Bypass           | `CTF{sql_1nj3ct10n_f0r_th3_w1n}`   |
| Find the Whistleblower | `CTF{gps_exif_metadata_leak}`      |
| Hidden in Plain Sight  | `CTF{st3g0_1s_not_s3cur1ty}`       |
| Stack Smash 101        | `CTF{buff3r_0v3rfl0w_pwn3d}`       |

---

## Environment Variables

Edit `docker-compose.yml` or create a `.env` file:

```env
SECRET_KEY=your-long-random-secret-key
DEBUG=False
DATABASE_URL=postgresql://ctfuser:ctfpassword123@db:5432/ctfdb
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=yourdomain.com,localhost
CTF_NAME=HackArena CTF
CTF_START=2025-06-01T00:00:00
CTF_END=2025-06-02T23:59:59
```

---

## Admin Features

All challenge management is done via `/admin/`:

- Create / edit / activate challenges
- Set flags (hashed with SHA-256 — never stored in plaintext)
- Upload challenge files
- Add hints with point costs
- View all submissions (including wrong flags + IP addresses)
- Toggle `is_active` per challenge to reveal them progressively

---

## Security Notes

- Flags are stored as **SHA-256 hashes** — never in plaintext
- **Rate limiting**: max 10 flag submissions per minute per player per challenge
- **Cooldown**: 5-second gap between submissions (anti-brute-force)
- **Challenge containers** are isolated from the main Django network
- All submissions (correct and wrong) are logged with IP address
- Input is stripped of whitespace before hashing

---

## Development (no Docker)

```bash
pip install -r requirements.txt
export DATABASE_URL=sqlite:///db.sqlite3
export REDIS_URL=redis://localhost:6379/0

python ctf/manage.py migrate
python ctf/manage.py createsuperuser
python ctf/manage.py seed_challenges
python ctf/manage.py runserver
```

> Note: For development without Redis, Django Channels will fall back to the
> in-memory layer. The live scoreboard will still work within a single process.

---

## Adding More Challenges

1. Create a `Challenge` in `/admin/` with `is_active=False`
2. Upload any files
3. Set the flag via admin (it's hashed automatically on save if you use the management command)
4. Flip `is_active=True` when ready to release

Or use the management command as a template: `ctf/apps/challenges/management/commands/seed_challenges.py`
