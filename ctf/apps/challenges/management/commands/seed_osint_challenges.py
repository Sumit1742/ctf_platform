"""
python manage.py seed_osint_challenges

Seeds 5 OSINT challenges (Easy → Hard) into the CTF platform.
Run once after migrations, or with --reset to refresh.

UPDATES (v2):
  - Lab 1 (GitHub Recon): targets the real repo https://github.com/Devyansh08/
    Flag placeholder = CTF{PLACEHOLDER} — replace with the actual flag you
    add to that repo before running this command.
  - Lab 2 (Google Dorking): now points to the self-hosted Flask site at :5006
    where /secret.txt is exposed. Players use site: / filetype: operators.
  - Lab 4 (Image Geolocation): updated flag to match the GPS-embedded image
    (India Gate, New Delhi). Image served at :5007/image
  - All data.pop('flag') calls now operate on a copy (re-run safe).
"""
from django.core.management.base import BaseCommand
from ctf.apps.challenges.models import Challenge


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ IMPORTANT — before running this command:                                │
# │  1. Add a file named FLAG.txt to https://github.com/Devyansh08/         │
# │     containing the flag below (or any repo/gist on that account).       │
# │  2. Change GITHUB_RECON_FLAG to whatever you put in the repo.           │
# └─────────────────────────────────────────────────────────────────────────┘
GITHUB_RECON_FLAG = 'CTF{d3vy4nsh_g1thub_r3c0n}'  # ← replace with real flag you add to repo


OSINT_CHALLENGES = [
    # ------------------------------------------------------------------ #
    # 1. EASY — GitHub Recon (100pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'GitHub Recon',
        'category': 'osint',
        'difficulty': 'easy',
        'points': 100,
        'flag': GITHUB_RECON_FLAG,
        'description': (
            "A developer left something interesting in their public GitHub profile.\n\n"
            "Target GitHub account: https://github.com/Devyansh08/\n\n"
            "Explore their repositories, README files, commit history, and any "
            "pinned repos or gists. The flag is hidden somewhere in their public profile.\n\n"
            "Note: The flag follows the standard CTF{ } format."
        ),
        'hints': [
            {
                'text': 'Start at the profile page. Check every public repository — README files, commits, and file contents.',
                'cost': 15,
            },
            {
                'text': 'Look inside repository files and commit history. Developers sometimes accidentally commit sensitive data.',
                'cost': 35,
            },
        ],
        'connection_info': 'https://github.com/Devyansh08/',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 2. EASY-MEDIUM — Google Dorking (150pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Google Dorking',
        'category': 'osint',
        'difficulty': 'easy',
        'points': 150,
        'flag': 'CTF{d0rk1ng_f1nds_s3cr3ts}',
        'description': (
            "A company called \"NovaTech Solutions\" accidentally left a sensitive file "
            "exposed on their web server. The file is a plain .txt document that was "
            "never meant to be public.\n\n"
            "They only removed it from the navigation menu — but the file is still there.\n\n"
            "Their site is running at: http://localhost:5006\n\n"
            "Use Google-style advanced search techniques to find the hidden file.\n\n"
            "Tip: Think about what operators let you search within a specific site "
            "for specific file types."
        ),
        'hints': [
            {
                'text': 'Web servers serve any file in their document root — even ones not linked in the menu. Some operator searches can reveal them.',
                'cost': 20,
            },
            {
                'text': 'Google operators: site: restricts search to one domain, filetype: filters by extension. But since this is local, try browsing to common paths like /secret.txt, /robots.txt, /sitemap.xml.',
                'cost': 50,
            },
        ],
        'connection_info': 'http://localhost:5006',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 3. MEDIUM — Wayback Machine (250pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Wayback Machine',
        'category': 'osint',
        'difficulty': 'medium',
        'points': 250,
        'flag': 'CTF{w4yb4ck_n3v3r_f0rg3ts}',
        'description': (
            "A website has been scrubbed clean — the owner deleted everything "
            "after realising they had exposed sensitive information.\n\n"
            "But the internet never truly forgets.\n\n"
            "The target site is: http://secretproject-ctf.com\n\n"
            "Find what was there before it was deleted.\n"
            "The flag was hidden on the /secret page back in 2022."
        ),
        'hints': [
            {
                'text': 'There are services that archive website snapshots over time. The Wayback Machine at web.archive.org is a good start.',
                'cost': 25,
            },
            {
                'text': 'Visit web.archive.org, search for the URL, and browse snapshots from 2022. Then navigate to /secret in that snapshot.',
                'cost': 60,
            },
        ],
        'connection_info': '',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 4. HARD — Image Geolocation (400pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Image Geolocation',
        'category': 'osint',
        'difficulty': 'hard',
        'points': 400,
        'flag': 'CTF{1nd14_g4t3_n3w_d3lh1}',
        'description': (
            "A suspect posted this image online before going dark.\n\n"
            "Download the image from: http://localhost:5007/image\n\n"
            "Your mission:\n"
            "  1. Analyse the image and its metadata\n"
            "  2. Identify the landmark and city where it was taken\n"
            "  3. Submit the flag as: CTF{landmark_city} in lowercase with underscores\n\n"
            "Example: CTF{eiffel_tower_paris}\n\n"
            "Tools: exiftool, Google Lens, or any EXIF viewer."
        ),
        'hints': [
            {
                'text': 'Look carefully at every detail — signs, architecture, and especially the image file metadata. Cameras often embed location data.',
                'cost': 50,
            },
            {
                'text': 'Run: exiftool suspicious.jpg — look for GPS coordinates. Then search those coordinates on Google Maps to identify the location.',
                'cost': 100,
            },
        ],
        'connection_info': 'http://localhost:5007',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 5. HARD — Whois & DNS Recon (500pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Whois Knows Everything',
        'category': 'osint',
        'difficulty': 'hard',
        'points': 500,
        'flag': 'CTF{wh01s_kn0ws_3v3ryth1ng}',
        'description': (
            "A threat actor registered a domain to host their C2 server. "
            "Intelligence suggests the registrant used their real email.\n\n"
            "Starting domain: malicious-c2-ctf.net\n\n"
            "Your mission:\n"
            "  1. Look up the WHOIS record for the domain\n"
            "  2. Find the registrant email address\n"
            "  3. Use that email to find their other registered domains\n"
            "  4. One of those domains has a TXT DNS record containing the flag\n\n"
            "Tools: whois, dnsdumpster.com, SecurityTrails, or ViewDNS.info"
        ),
        'hints': [
            {
                'text': 'WHOIS records contain registration information. Threat actors sometimes reuse the same email across multiple domains.',
                'cost': 75,
            },
            {
                'text': 'Once you have the email, pivot — search for all domains registered with that email using ViewDNS or SecurityTrails. Then check TXT records: dig TXT domain.com',
                'cost': 150,
            },
        ],
        'connection_info': '',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed 5 OSINT challenges (Easy → Hard)  [v2 — GitHub Recon, Dorking site, Geo image]'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing OSINT challenges before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = Challenge.objects.filter(category='osint').delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing OSINT challenge(s).'))

        created = updated = 0

        for data in OSINT_CHALLENGES:
            # copy() prevents KeyError on repeated runs (data.pop mutates module-level dict)
            data = data.copy()
            raw_flag = data.pop('flag')
            ch, was_created = Challenge.objects.update_or_create(
                title=data['title'],
                defaults=data,
            )
            ch.set_flag(raw_flag)
            ch.save()

            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✔ Created : {ch.title}  ({ch.points} pts)'))
            else:
                updated += 1
                self.stdout.write(f'  ↻ Updated : {ch.title}  ({ch.points} pts)')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone — {created} created, {updated} updated.'
        ))
        self.stdout.write(self.style.WARNING(
            '\n⚠  REMINDER: Add the real flag to https://github.com/Devyansh08/ '
            'and update GITHUB_RECON_FLAG in this file before running on production.'
        ))
