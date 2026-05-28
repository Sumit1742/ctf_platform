"""
python manage.py seed_challenges

Seeds all 5 CTF challenges with correct flags.
Run this once after migrations.
"""
from django.core.management.base import BaseCommand
from ctf.apps.challenges.models import Challenge


CHALLENGES = [
    {
        'title': "Caesar's Last Secret",
        'category': 'crypto',
        'difficulty': 'easy',
        'points': 100,
        'flag': 'CTF{caesar_cipher_is_too_old}',
        'description': (
            "A Roman general left an encrypted message before his assassination.\n"
            "Decrypt it to find what he was hiding.\n\n"
            "Encrypted message:\n"
            "  PGS{prnfne_pvcure_vf_gbb_byq}\n\n"
            "The flag is in the standard format: CTF{...}"
        ),
        'hints': [
            {'text': 'ROT13 is a special case of Caesar cipher.', 'cost': 10},
            {'text': 'Try all 26 possible shifts. One of them will produce readable text.', 'cost': 25},
        ],
        'connection_info': '',
        'is_active': True,
    },
    {
        'title': 'Login Bypass',
        'category': 'web',
        'difficulty': 'medium',
        'points': 200,
        'flag': 'CTF{sql_1nj3ct10n_f0r_th3_w1n}',
        'description': (
            "A poorly written admin login page is protecting a secret panel.\n"
            "Can you get in without knowing the password?\n\n"
            "The application is running at the address below.\n"
            "Your goal: log in as admin and retrieve the flag."
        ),
        'hints': [
            {'text': "Try injecting SQL into the username field.", 'cost': 20},
            {'text': "Classic payload: ' OR '1'='1' --", 'cost': 50},
        ],
        'connection_info': 'http://localhost:5001',
        'is_active': True,
    },
    {
        'title': 'Find the Whistleblower',
        'category': 'osint',
        'difficulty': 'medium',
        'points': 250,
        'flag': 'CTF{gps_exif_metadata_leak}',
        'description': (
            "A fictional researcher leaked classified documents and went into hiding.\n"
            "They posted one last photo online before going dark.\n\n"
            "Using only public information and the attached image,\n"
            "find their location — then submit the flag.\n\n"
            "Download the image file and investigate it carefully.\n"
            "The flag is hidden inside the file itself."
        ),
        'hints': [
            {'text': 'Images can contain hidden metadata you cannot see with the naked eye.', 'cost': 25},
            {'text': 'Try: exiftool suspicious.jpg — look for GPS coordinates.', 'cost': 50},
        ],
        'connection_info': '',
        'is_active': True,
    },
    {
        'title': 'Hidden in Plain Sight',
        'category': 'forensics',
        'difficulty': 'medium',
        'points': 300,
        'flag': 'CTF{st3g0_1s_not_s3cur1ty}',
        'description': (
            "Someone hid a secret inside this innocent-looking image file.\n"
            "The image looks completely normal, but something is lurking beneath the pixels.\n\n"
            "Download suspicious.png and find what is hidden inside.\n\n"
            "The flag format is CTF{...}"
        ),
        'hints': [
            {'text': 'Steganography is the art of hiding data inside other data.', 'cost': 30},
            {'text': 'LSB (Least Significant Bit) encoding is a common technique for PNG files. Try zsteg or write your own decoder.', 'cost': 75},
        ],
        'connection_info': '',
        'is_active': True,
    },
    {
        'title': 'Stack Smash 101',
        'category': 'pwn',
        'difficulty': 'hard',
        'points': 500,
        'flag': 'CTF{buff3r_0v3rfl0w_pwn3d}',
        'description': (
            "A simple C service with a classic vulnerability.\n"
            "Overflow the buffer, hijack the return address,\n"
            "and redirect execution to the win() function.\n\n"
            "Binary and source code are provided as attachments.\n"
            "Remote service is running at the address below.\n\n"
            "Protections: No stack canary, No NX, No PIE (32-bit)."
        ),
        'hints': [
            {'text': "This is a classic stack buffer overflow. Find the offset to the saved return address.", 'cost': 50},
            {'text': "Use Python + pwntools. The win() address is printed at startup — no need to calculate it.", 'cost': 100},
        ],
        'connection_info': 'nc localhost 4444',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with 5 CTF challenges'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete existing challenges first')

    def handle(self, *args, **options):
        if options['reset']:
            Challenge.objects.all().delete()
            self.stdout.write(self.style.WARNING('Deleted all existing challenges.'))

        created = 0
        updated = 0

        for data in CHALLENGES:
            flag = data.pop('flag')
            ch, was_created = Challenge.objects.update_or_create(
                title=data['title'],
                defaults=data,
            )
            ch.set_flag(flag)
            ch.save()

            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {ch.title}'))
            else:
                updated += 1
                self.stdout.write(f'  Updated: {ch.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created} created, {updated} updated.'
        ))
        self.stdout.write(
            'Remember to create challenge files (OSINT image, stego PNG, pwn binary) '
            'and attach them via the Django admin.'
        )
