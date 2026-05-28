"""
python manage.py seed_crypto_challenges

Seeds 5 Crypto challenges (Easy → Hard) into the CTF platform.
Run once after migrations, or with --reset to refresh.

FIXES (v2):
  - data.pop('flag') now done on a copy so re-runs never raise KeyError.
  - Lab 2 (Hash Cracking): regenerated hashes that actually decode to the flag.
"""
from django.core.management.base import BaseCommand
from ctf.apps.challenges.models import Challenge


CRYPTO_CHALLENGES = [
    # ------------------------------------------------------------------ #
    # 1. EASY — Base Confusion (150pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Base Confusion',
        'category': 'crypto',
        'difficulty': 'easy',
        'points': 150,
        'flag': 'CTF{b4s3_3nc0d1ng_1s_n0t_3ncrypt10n}',
        'description': (
            "We intercepted this string — but it looks like someone wrapped it "
            "in layers before sending.\n\n"
            "Encoded message:\n"
            "R1FaVEtOQlVHWTNVRU5SU0dNMkRPTVpUR00yVU1NWlRHWkNUTU1aVEdBM0RJTVpSR1pDVE1OWlZJWVpUQ05aVEdWRERNUkpUR0EzVElOS0dHTVpUTVJKV0dNM1RFTlpaRzRZRE9OQlRHRVpUQU5TRkc1Q0E9PT09\n\n"
            "Peel back every layer to find the flag.\n\n"
            "Hint: there are exactly three encoding layers. Identify each one."
        ),
        'hints': [
            {
                'text': 'Encoding is not encryption. The character set of a string usually reveals what encoding was used.',
                'cost': 20,
            },
            {
                'text': 'Layer 1 → Base64 decode. Layer 2 → Base32 decode. Layer 3 → Hex (Base16) decode.',
                'cost': 40,
            },
        ],
        'connection_info': '',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 2. MEDIUM — Hash Cracking (200pts)  ← FIXED: hashes now match flag
    # ------------------------------------------------------------------ #
    {
        'title': 'Hash Cracking',
        'category': 'crypto',
        'difficulty': 'medium',
        'points': 200,
        'flag': 'CTF{hashes_are_not_secure_alone}',
        'description': (
            "We found a list of MD5 hashes. Each hash encodes a single common English word.\n"
            "Crack all five, read them in order, and wrap them as: CTF{word1_word2_word3_word4_word5}\n\n"
            "Hashes:\n"
            "  1. ad13e3e85208780288a2389c791b5c03\n"
            "  2. 4015e9ce43edfb0668ddaa973ebc7e87\n"
            "  3. d529e941509eb9e9b9cfaeae1fe7ca23\n"
            "  4. 1c0b76fce779f78f51be339c49445c49\n"
            "  5. c42bbd90740264d115048a82c9a10214\n\n"
            "Submit the flag in the format: CTF{word1_word2_word3_word4_word5}"
        ),
        'hints': [
            {
                'text': 'MD5 is fast and has no salt here. Precomputed lookup tables exist for common English words.',
                'cost': 25,
            },
            {
                'text': 'Try an online MD5 reverse lookup (e.g. md5decrypt.net), or run: hashcat -a 0 -m 0 hashes.txt /usr/share/wordlists/rockyou.txt',
                'cost': 50,
            },
        ],
        'connection_info': '',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 3. MEDIUM — XOR Secrets (250pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'XOR Secrets',
        'category': 'crypto',
        'difficulty': 'medium',
        'points': 250,
        'flag': 'CTF{x0r_1s_symm3tr1c_m4g1c}',
        'description': (
            "A secret message was encrypted using XOR with a single-byte key.\n"
            "The result was hex-encoded.\n\n"
            "Ciphertext (hex):\n"
            "011604393a72301d73311d313b2f2f71363073211d2f762573213f\n\n"
            "Find the key, decrypt the message, and submit the flag."
        ),
        'hints': [
            {
                'text': 'XOR with the same key twice restores the original. The key is a single byte (0–255).',
                'cost': 25,
            },
            {
                'text': 'Brute-force all 256 possible keys and look for readable ASCII output. The flag always starts with CTF{.',
                'cost': 60,
            },
        ],
        'connection_info': '',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 4. HARD — RSA Small Exponent (400pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'RSA Small Exponent',
        'category': 'crypto',
        'difficulty': 'hard',
        'points': 400,
        'flag': 'CTF{sm4ll_3xp0n3nt_b1g_m1st4k3}',
        'description': (
            "We captured an RSA-encrypted message. Something looks off about the public key.\n\n"
            "Public key:\n"
            "  n = 179769313486231590772930519078902473361797697894230657273430081157732675805502515650800778031342685000608576382426650243675906465425555674530873481592165113550026672087096385218852090143011078094501538315451057488366235256443849371457544103074132158615850022581027136881515050196403045352966622945220856139471\n"
            "  e = 3\n\n"
            "Ciphertext:\n"
            "  c = 1683477242754478900349672997451837560437292233620605214313283508472368611434321527418929579130845042300100153175940731341041419234105328289835198206477087826599017215396774021227032303460266357753442040204696017664019017317\n\n"
            "Recover the plaintext and submit the flag."
        ),
        'hints': [
            {
                'text': 'RSA encryption: c = m^e mod n. When e is very small and the plaintext is short, think about what happens mathematically.',
                'cost': 60,
            },
            {
                'text': 'If the plaintext m is small enough, m^3 < n — meaning no modular reduction occurred. Just take the integer cube root of c.',
                'cost': 120,
            },
        ],
        'connection_info': '',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 5. HARD — Vigenère Known Plaintext (500pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Vigenère Known Plaintext',
        'category': 'crypto',
        'difficulty': 'hard',
        'points': 500,
        'flag': 'CTF{v1g3n3r3_k3y_r3c0v3ry}',
        'description': (
            "A secret message was encrypted with a Vigenère cipher.\n"
            "You know the flag format always starts with CTF{ — use that.\n\n"
            "Ciphertext:\n"
            "  JTH{f1n3n3t3_u3f_r3e0f3yy}\n\n"
            "The key is a common English word in ALL CAPS.\n"
            "Recover the key and decrypt the full message to get the flag."
        ),
        'hints': [
            {
                'text': 'You already know the first four characters of the plaintext. Compare them with the ciphertext at the same positions to derive the key characters.',
                'cost': 75,
            },
            {
                'text': 'Vigenère works letter-by-letter with a repeating key. Key char = (CT_char - PT_char) mod 26. The key repeats — find its length from the pattern.',
                'cost': 150,
            },
        ],
        'connection_info': '',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed 5 Crypto challenges (Easy → Hard)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing crypto challenges before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = Challenge.objects.filter(category='crypto').delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing crypto challenge(s).'))

        created = updated = 0

        for data in CRYPTO_CHALLENGES:
            # Use a copy so re-running never raises KeyError on the popped 'flag' key
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
