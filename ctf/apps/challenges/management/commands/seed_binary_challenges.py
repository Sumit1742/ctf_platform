"""
python manage.py seed_binary_challenges

Seeds 5 Binary / Pwn challenges (Easy → Hard) into the CTF platform.
Run once after migrations, or with --reset to refresh.
"""
from django.core.management.base import BaseCommand
from ctf.apps.challenges.models import Challenge


BINARY_CHALLENGES = [
    # ------------------------------------------------------------------ #
    # 1. EASY — Strings Hunt (100pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Strings Hunt',
        'category': 'pwn',
        'difficulty': 'easy',
        'points': 100,
        'flag': 'CTF{str1ngs_c0mm4nd_r3v34ls_s3cr3ts}',
        'description': (
            "A binary was found on a compromised machine.\n\n"
            "Download: http://localhost:5012/strings_hunt\n\n"
            "The developer embedded the flag directly inside the binary "
            "as a readable string — they just hoped nobody would look.\n\n"
            "Find it without running the program."
        ),
        'hints': [
            {
                'text': 'Compiled binaries often contain human-readable text. There is a classic Linux tool named after exactly what you need to do.',
                'cost': 15,
            },
            {
                'text': 'Run: `strings strings_hunt | grep CTF` — the strings command extracts all printable character sequences from a binary.',
                'cost': 30,
            },
        ],
        'connection_info': 'http://localhost:5012',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 2. EASY-MEDIUM — Buffer Overflow (150pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Stack Smasher',
        'category': 'pwn',
        'difficulty': 'easy',
        'points': 150,
        'flag': 'CTF{buff3r_0v3rfl0w_w1ns_4g41n}',
        'description': (
            "A vulnerable service is running — it reads your name and greets you.\n\n"
            "Connect: nc localhost 4001\n\n"
            "The program uses a fixed-size buffer but never checks how much you send.\n"
            "There is a hidden function called win() that prints the flag.\n"
            "It is never called in normal execution — but you can change that.\n\n"
            "Download the binary for analysis: http://localhost:5012/stack_smasher"
        ),
        'hints': [
            {
                'text': 'When you write more data than a buffer can hold, you overwrite adjacent memory — including the return address.',
                'cost': 25,
            },
            {
                'text': 'Use `gdb` or `pwndbg` to find the offset to the return address. Then overwrite it with the address of win(). Try: `python3 -c "print(\'A\'*offset + win_addr)" | nc localhost 4001`',
                'cost': 60,
            },
        ],
        'connection_info': 'nc localhost 4001',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 3. MEDIUM — Format String (250pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Format Flaw',
        'category': 'pwn',
        'difficulty': 'medium',
        'points': 250,
        'flag': 'CTF{pr1ntf_1s_d4ng3r0us}',
        'description': (
            "A service echoes back whatever you send — using printf() directly.\n\n"
            "Connect: nc localhost 4002\n\n"
            "The flag is stored in a local variable on the stack.\n"
            "Normal input won't reveal it — but printf has a secret power "
            "when given the right format specifiers.\n\n"
            "Download the binary: http://localhost:5012/format_flaw"
        ),
        'hints': [
            {
                'text': 'printf() treats its first argument as a format string. What happens when user input becomes the format string?',
                'cost': 30,
            },
            {
                'text': 'Send format specifiers like %x, %s, %p to leak stack values. The flag is on the stack — keep leaking until you find it: `%1$p %2$p %3$p ...`',
                'cost': 75,
            },
        ],
        'connection_info': 'nc localhost 4002',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 4. HARD — Ret2Win (400pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'Return to Win',
        'category': 'pwn',
        'difficulty': 'hard',
        'points': 400,
        'flag': 'CTF{r3t_t0_w1n_cl4ss1c}',
        'description': (
            "Classic ret2win — with a twist. Stack canaries are enabled.\n\n"
            "Connect: nc localhost 4003\n\n"
            "The binary has:\n"
            "  - A stack canary (you need to leak it first)\n"
            "  - A win() function that calls system('/bin/sh')\n"
            "  - A format string vulnerability to leak the canary\n"
            "  - A buffer overflow to control execution\n\n"
            "Two-stage exploit: leak the canary, then overflow.\n\n"
            "Download the binary: http://localhost:5012/ret2win"
        ),
        'hints': [
            {
                'text': 'Stack canaries are random values placed before the return address. Overwriting them triggers an abort — unless you already know the value.',
                'cost': 60,
            },
            {
                'text': 'Stage 1: use the format string bug to leak the canary value. Stage 2: craft your payload as [padding + canary + padding + win_addr].',
                'cost': 130,
            },
        ],
        'connection_info': 'nc localhost 4003',
        'is_active': True,
    },

    # ------------------------------------------------------------------ #
    # 5. HARD — GOT Overwrite (500pts)
    # ------------------------------------------------------------------ #
    {
        'title': 'GOT Hijack',
        'category': 'pwn',
        'difficulty': 'hard',
        'points': 500,
        'flag': 'CTF{g0t_0v3rwr1t3_pwn3d}',
        'description': (
            "Full RELRO is off. The GOT is writable.\n\n"
            "Connect: nc localhost 4004\n\n"
            "The binary calls exit() after your input — but what if exit() "
            "suddenly pointed somewhere else?\n\n"
            "Your goal:\n"
            "  1. Leak a libc address using the format string vulnerability\n"
            "  2. Calculate libc base and the address of system()\n"
            "  3. Overwrite GOT[exit] with system()\n"
            "  4. Send /bin/sh as input — it becomes the argument to system()\n\n"
            "Download the binary: http://localhost:5012/got_hijack"
        ),
        'hints': [
            {
                'text': 'The Global Offset Table (GOT) maps library function names to their real addresses in memory. If it is writable, you can redirect any function call.',
                'cost': 80,
            },
            {
                'text': 'Leak libc with %p format strings to find base address. Then: system_addr = libc_base + system_offset. Overwrite with: `fmtstr_payload(offset, {got_exit: system_addr})`',
                'cost': 180,
            },
        ],
        'connection_info': 'nc localhost 4004',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed 5 Binary/Pwn challenges (Easy → Hard)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing pwn challenges before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = Challenge.objects.filter(category='pwn').delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing pwn challenge(s).'))

        created = updated = 0

        for data in BINARY_CHALLENGES:
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
