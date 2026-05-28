#!/usr/bin/env bash
# =============================================================
#  HackArena CTF — Quick Setup Script
#  Run this once after cloning the repo.
#  Usage: bash scripts/setup.sh
# =============================================================

set -e
cd "$(dirname "$0")/.."

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${CYAN}[*]${NC} $1"; }
ok()   { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   HackArena CTF — Setup Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# --- 1. Check Python ---
log "Checking Python..."
python3 --version || err "Python 3 not found"
ok "Python OK"

# --- 2. Virtual environment ---
if [ ! -d "venv" ]; then
    log "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
ok "Virtual environment active"

# --- 3. Install Python deps ---
log "Installing Python dependencies..."
pip install -q -r requirements.txt
ok "Dependencies installed"

# --- 4. Run migrations ---
log "Running Django migrations..."
cd ctf
python manage.py makemigrations accounts --settings=ctf.settings
python manage.py makemigrations challenges --settings=ctf.settings
python manage.py makemigrations submissions --settings=ctf.settings
python manage.py makemigrations scoreboard --settings=ctf.settings
python manage.py migrate --settings=ctf.settings
ok "Database migrated"

# --- 5. Seed challenges ---
log "Seeding CTF challenges..."
python manage.py seed_challenges --settings=ctf.settings
ok "Challenges seeded"

# --- 6. Create superuser ---
log "Creating admin superuser..."
warn "You will be prompted to set a password."
python manage.py createsuperuser --settings=ctf.settings || warn "Superuser may already exist"

# --- 7. Collect static files ---
log "Collecting static files..."
python manage.py collectstatic --noinput --settings=ctf.settings
ok "Static files collected"

cd ..

# --- 8. Create challenge asset files ---
log "Creating OSINT challenge image..."
python scripts/create_osint_image.py || warn "OSINT image creation failed (install: pip install piexif)"

log "Creating Steganography challenge image..."
python scripts/create_stego_image.py || warn "Stego image creation failed (install: pip install Pillow)"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "  Start dev server:     ${CYAN}cd ctf && python manage.py runserver${NC}"
echo -e "  Admin panel:          ${CYAN}http://localhost:8000/admin${NC}"
echo -e "  Challenges:           ${CYAN}http://localhost:8000/challenges/${NC}"
echo -e "  Scoreboard:           ${CYAN}http://localhost:8000/scoreboard/${NC}"
echo ""
echo -e "  For full stack with Docker:"
echo -e "    ${CYAN}docker-compose up --build${NC}"
echo ""
warn "Don't forget to upload challenge files in the admin panel:"
warn "  - OSINT:     media/challenge_files/suspicious.jpg"
warn "  - Forensics: media/challenge_files/suspicious.png"
warn "  - PWN:       compile vuln.c and upload the binary"
echo ""
