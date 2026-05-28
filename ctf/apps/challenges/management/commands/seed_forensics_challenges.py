"""
python manage.py seed_forensics_challenges

Seeds 5 Forensics challenges (Easy → Hard) into the CTF platform.
Run once after migrations, or with --reset to refresh.
"""
from django.core.management.base import BaseCommand
from ctf.apps.challenges.models import Challenge


FORENSICS_CHALLENGES = [
    # ------------------------------------------------------------------ #
    # 1. EASY — Magic Bytes (100pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Not What It Seems',
        'category': 'forensics',
        'difficulty': 'easy',
        'points': 100,
        'flag': 'CTF{m4g1c_byt3s_d0nt_l13}',
        'description': (
            "We received a file called `secret.txt` from an unknown source.\n\n"
            "Download: http://localhost:5011/secret.txt\n\n"
            "Something feels off. Open it in a text editor and you'll see "
            "it's not plain text at all.\n\n"
            "Every file format has a true identity buried somewhere inside it. "
            "Find what this file really is — then figure out how to properly "
            "read its contents to retrieve the flag.\n\n"
            "The flag is not on the surface."
        ),
        'hints': [
            {
                'text': (
                    "File extensions are just labels — the OS can be lied to. "
                    "What actually identifies a file's true format at the binary level?"
                ),
                'cost': 15,
            },
            {
                'text': (
                    "Once you know the real file type, think about what structured "
                    "data that format can carry beyond its main content. "
                    "Not everything is visible to the naked eye."
                ),
                'cost': 40,
            },
        ],
        'connection_info': 'http://localhost:5011',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 2. MEDIUM — EXIF Metadata (200pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Metadata Leak',
        'category': 'forensics',
        'difficulty': 'medium',
        'points': 200,
        'flag': 'CTF{3x1f_d4t4_t3lls_4ll}',
        'description': (
            "A photo was recovered from a suspect's device.\n\n"
            "Download: http://localhost:5011/photo.jpg\n\n"
            "Image files carry far more than just pixels. Cameras, phones, "
            "and processing software all leave traces.\n\n"
            "This particular image has something hidden across multiple "
            "non-standard metadata segments. A single tool pass may not "
            "show you everything — you'll need to look deeper and "
            "reassemble what you find.\n\n"
            "The flag is not in the image itself."
        ),
        'hints': [
            {
                'text': (
                    "JPEG files support many different application-specific marker "
                    "segments beyond the standard EXIF block. Some tools only show "
                    "the most common ones."
                ),
                'cost': 25,
            },
            {
                'text': (
                    "When you find the hidden segments, the data inside may need "
                    "one more transformation before it becomes readable. "
                    "Look at all segments, not just the first one."
                ),
                'cost': 60,
            },
        ],
        'connection_info': 'http://localhost:5011',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 3. MEDIUM — LSB Steganography (300pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Hidden in Plain Sight',
        'category': 'forensics',
        'difficulty': 'medium',
        'points': 300,
        'flag': 'CTF{lsb_st3g0_h1dd3n_1n_p1x3ls}',
        'description': (
            "Just a sunset. Nothing special.\n\n"
            "Download: http://localhost:5011/sunset.png\n\n"
            "Or is it?\n\n"
            "Someone embedded a secret in this image using the oldest trick "
            "in the steganography book — but they added their own twist to "
            "make sure off-the-shelf tools wouldn't find it on the first try.\n\n"
            "You'll need to write your own extractor. Think carefully about "
            "where the data starts and what state it's in when you pull it out."
        ),
        'hints': [
            {
                'text': (
                    "LSB steganography hides data in the least significant bits "
                    "of pixel values. But the embedding doesn't have to start "
                    "at the very first pixel."
                ),
                'cost': 35,
            },
            {
                'text': (
                    "Even after you extract the raw bits correctly, the result "
                    "may not be immediately readable. A short repeating key "
                    "might have been applied before hiding."
                ),
                'cost': 80,
            },
        ],
        'connection_info': 'http://localhost:5011',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 4. HARD — DNS Exfiltration PCAP (450pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Packet Detective',
        'category': 'forensics',
        'difficulty': 'hard',
        'points': 450,
        'flag': 'CTF{p4ck3t_sniff3r_s33s_4ll}',
        'description': (
            "We captured network traffic from a machine suspected of leaking data.\n\n"
            "Download: http://localhost:5011/capture.pcap\n\n"
            "The analyst who reviewed it said: "
            "\"I checked the HTTP traffic — nothing there.\"\n\n"
            "Look harder. The exfiltration is real, it's just not where "
            "most people look first.\n\n"
            "The flag was sent out in pieces. You need to find all of them "
            "and put them back together in the right order."
        ),
        'hints': [
            {
                'text': (
                    "HTTP isn't the only protocol that carries data outbound. "
                    "Attackers often use protocols that are harder to block "
                    "and easier to hide in."
                ),
                'cost': 50,
            },
            {
                'text': (
                    "The pieces are numbered. Once you filter to the right "
                    "traffic type, look at the structure of the queries — "
                    "the data is encoded in a way that makes it look legitimate "
                    "at a glance."
                ),
                'cost': 120,
            },
        ],
        'connection_info': 'http://localhost:5011',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 5. HARD — Password Protected ZIP (550pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Locked Archive',
        'category': 'forensics',
        'difficulty': 'hard',
        'points': 550,
        'flag': 'CTF{z1p_p4ssw0rd_cr4ck3d}',
        'description': (
            "A ZIP archive was recovered from a seized device.\n\n"
            "Download: http://localhost:5011/secret.zip\n\n"
            "It's password protected. The password isn't a dictionary word — "
            "it follows a pattern. A README inside the archive (once you crack "
            "it) will tell you the policy that was used to create it.\n\n"
            "And cracking the password is only half the job.\n\n"
            "Once you're inside, don't trust everything you see. "
            "Read every file carefully — one of them has the real flag, "
            "but it won't be handed to you plainly."
        ),
        'hints': [
            {
                'text': (
                    "Standard wordlist attacks won't work here. The password "
                    "was created by taking a base word and applying transformation "
                    "rules. Think about what rules hashcat or similar tools support."
                ),
                'cost': 70,
            },
            {
                'text': (
                    "There's more than one file inside. Not all of them are "
                    "what they appear to be. One file describes the encoding "
                    "used to protect the real flag — that's the one you want."
                ),
                'cost': 160,
            },
        ],
        'connection_info': 'http://localhost:5011',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed 5 Forensics challenges (Easy → Hard)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing forensics challenges before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = Challenge.objects.filter(category='forensics').delete()
            self.stdout.write(self.style.WARNING(
                f'Deleted {deleted} existing forensics challenge(s).'))

        created = updated = 0

        for data in FORENSICS_CHALLENGES:
            raw_flag = data.pop('flag')

            ch, was_created = Challenge.objects.update_or_create(
                title=data['title'],
                defaults=data,
            )
            ch.set_flag(raw_flag)
            ch.save()

            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  ✔ Created : {ch.title}  ({ch.points} pts)'))
            else:
                updated += 1
                self.stdout.write(
                    f'  ↻ Updated : {ch.title}  ({ch.points} pts)')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone — {created} created, {updated} updated.'))