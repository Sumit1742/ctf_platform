from django.core.management.base import BaseCommand
from ctf.apps.challenges.models import Challenge

WEB_CHALLENGES = [
    {
        'title': 'SQL Login Bypass',
        'category': 'web', 'difficulty': 'easy', 'points': 100,
        'flag': 'CTF{sql_1nj3ct10n_f0r_th3_w1n}',
        'description': (
            "A login page protects the admin panel.\n"
            "The developer trusted user input a little too much.\n\n"
            "Can you log in as admin without knowing the password?\n\n"
            "Target: http://localhost:5000"
        ),
        'hints': [
            {'text': 'Think about how the server builds its SQL query using what you type.', 'cost': 20},
            {'text': "Try entering ' OR '1'='1 as the username with any password.", 'cost': 50},
        ],
        'connection_info': 'http://localhost:5000',
        'is_active': True,
    },
    {
        'title': 'Session Hijacking',
        'category': 'web', 'difficulty': 'easy', 'points': 100,
        'flag': 'CTF{s3ss10n_h1j4ck1ng_1s_d4ng3r0us}',
        'description': (
            "This web app uses predictable session tokens for authentication.\n"
            "Log in as guest (guest / guest) and examine your session cookie.\n\n"
            "The admin has an active session. Find it and steal the flag.\n\n"
            "Target: http://localhost:5001"
        ),
        'hints': [
            {'text': 'Open DevTools → Application → Cookies. Look at your session_id value carefully.', 'cost': 10},
            {'text': 'Session IDs are assigned sequentially. Try incrementing or enumerating nearby values.', 'cost': 25},
        ],
        'connection_info': 'http://localhost:5001',
        'is_active': True,
    },
    {
        'title': 'Reflected Chaos',
        'category': 'web', 'difficulty': 'medium', 'points': 250,
        'flag': 'CTF{r3fl3ct3d_xss_n0_s4n1t1z4t10n}',
        'description': (
            "A search page reflects your input directly into the HTML response — unsanitised.\n\n"
            "Inject a payload that calls /flag?xss=1 when executed in the browser.\n\n"
            "Target: http://localhost:5003"
        ),
        'hints': [
            {'text': 'What happens when raw user input is placed inside an HTML page?', 'cost': 25},
            {'text': 'If <script> is filtered, try an event handler: <img src=x onerror="fetch(\'/flag?xss=1\')">',
             'cost': 60},
        ],
        'connection_info': 'http://localhost:5003',
        'is_active': True,
    },
    {
        'title': 'Path Traverser',
        'category': 'web', 'difficulty': 'hard', 'points': 400,
        'flag': 'CTF{p4th_tr4v3rs4l_0ut_0f_b0unds}',
        'description': (
            "A file-download endpoint has multiple filter layers — but one bypass remains.\n\n"
            "Filters applied (in order):\n"
            "  1. Strip leading /\n"
            "  2. Remove ../ sequences\n"
            "  3. URL-decode once\n\n"
            "The flag is at /flag.txt on the server.\n\n"
            "Example: GET /download?file=report.pdf\n\n"
            "Target: http://localhost:5002"
        ),
        'hints': [
            {'text': 'The filter runs on the decoded input. What if you encoded the traversal sequence twice?', 'cost': 50},
            {'text': 'Try: /download?file=..%252f..%252f..%252fflag.txt  (%25 encodes %, so %252f → %2f → /)', 'cost': 100},
        ],
        'connection_info': 'http://localhost:5002',
        'is_active': True,
    },
    {
        'title': 'Template Takeover',
        'category': 'web', 'difficulty': 'hard', 'points': 400,
        'flag': 'CTF{sst1_jinja2_rce_via_mro_chain}',
        'description': (
            "A Flask app renders your input directly inside a Jinja2 template string.\n"
            "A basic blacklist was added — but it is trivially bypassed.\n\n"
            "Verify injection: ?name={{7*7}} should return 49.\n"
            "Then walk the MRO chain to read the FLAG environment variable.\n\n"
            "Target: http://localhost:5004"
        ),
        'hints': [
            {'text': 'Confirm SSTI first with {{7*7}}. Then try accessing Python objects via __class__.', 'cost': 50},
            {'text': 'The blacklist blocks __class__ literally. Bypass with: {{""| attr("__class__")| attr("__mro__")}}', 'cost': 100},
        ],
        'connection_info': 'http://localhost:5004',
        'is_active': True,
    },
    {
        'title': 'Web Token Trickery',
        'category': 'web', 'difficulty': 'hard', 'points': 500,
        'flag': 'CTF{jwt_4lg_n0n3_4nd_w34k_s3cr3t}',
        'description': (
            "This API issues JWT tokens. The implementation has two vulnerabilities.\n\n"
            "Attack 1 — alg:none:\n"
            "  Fetch GET /api/token, decode the JWT, set alg=none in header,\n"
            "  change role to admin, remove the signature. Send with empty sig.\n\n"
            "Attack 2 — Weak HS256 secret:\n"
            "  The signing secret is a common dictionary word.\n"
            "  Crack it with jwt-cracker or hashcat, re-sign with role=admin.\n\n"
            "Either path → GET /api/admin with your forged token → flag.\n\n"
            "Target: http://localhost:5005"
        ),
        'hints': [
            {'text': 'A JWT is three base64url parts: header.payload.signature — all readable without a key.', 'cost': 75},
            {'text': 'Some libraries accept alg=none with no signature. Try: header={alg:none} + payload={role:admin} + empty signature.', 'cost': 150},
        ],
        'connection_info': 'http://localhost:5005',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed Web challenges (replaces Cookie Monster → Session Hijacking, Forbidden Files → Path Traverser)'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete existing web challenges first')

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = Challenge.objects.filter(category='web').delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} web challenge(s).'))

        created = updated = 0
        for data in WEB_CHALLENGES:
            raw_flag = data.pop('flag')
            ch, was_created = Challenge.objects.update_or_create(title=data['title'], defaults=data)
            ch.set_flag(raw_flag)
            ch.save()
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✔ Created : {ch.title} ({ch.points} pts)'))
            else:
                updated += 1
                self.stdout.write(f'  ↻ Updated : {ch.title} ({ch.points} pts)')

        self.stdout.write(self.style.SUCCESS(f'\nDone — {created} created, {updated} updated.'))
