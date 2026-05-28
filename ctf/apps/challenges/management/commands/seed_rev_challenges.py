from django.core.management.base import BaseCommand
from ctf.apps.challenges.models import Challenge

REV_CHALLENGES = [
    {
        'title': 'Dead Signal',
        'category': 'rev',
        'difficulty': 'easy',
        'points': 100,
        'flag': 'CTF{d34d_c0d3_n3v3r_l13s}',
        'description': (
            "During the raid on a NIGHTFALL safe house, investigators seized a laptop "
            "running an authentication daemon called agent_verify.\n\n"
            "The daemon was used to verify field agent identities before transmitting "
            "classified operation details. The source code was wiped — only the compiled "
            "binary survived.\n\n"
            "Intel suggests the binary was compiled in a hurry. The developer may not have "
            "taken precautions to protect sensitive strings in the final executable.\n\n"
            "The binary challenges you with a prompt:\n"
            "  agent@nightfall:~$\n\n"
            "Your task is to recover the correct identity token and submit it.\n\n"
            "Retrieve the artifact from the NIGHTFALL terminal.\n"
            "The operation HMAC key is: nightfall_op_2024\n"
            "Artifact name: agent_verify"
        ),
        'hints': [
            {'text': 'A binary compiled without precautions often leaks information. Static analysis tools can reveal what is embedded in the executable without running it.', 'cost': 20},
            {'text': 'Multiple strings in the binary look like flags. Not all of them are real. The real secret is encoded — look for patterns that differ from the obvious ones.', 'cost': 50},
        ],
        'connection_info': 'http://localhost:5016',
        'is_active': True,
    },
    {
        'title': 'Vault Protocol',
        'category': 'rev',
        'difficulty': 'medium',
        'points': 250,
        'flag': 'CTF{l1c3ns3_v4ul7_cr4ck3d}',
        'description': (
            "NIGHTFALL operated a physical vault at their headquarters, protected by "
            "a custom software lock — vault_access.\n\n"
            "The program accepts a 19-character authorization code and unlocks the vault "
            "if the code is valid. The format is four groups separated by dashes.\n\n"
            "The vault was decommissioned after the raid and the authorization codes were "
            "never recovered. All that remains is the binary itself.\n\n"
            "An intercepted communication mentioned:\n"
            "  'The code validation uses four independent verification routines.\n"
            "   Each group is checked by a different mathematical operation.\n"
            "   No two groups use the same method.'\n\n"
            "Reverse engineer the validation logic and find the correct authorization code "
            "to unlock the vault and retrieve the flag.\n\n"
            "Retrieve the artifact from the NIGHTFALL terminal.\n"
            "The operation HMAC key is: nightfall_op_2024\n"
            "Artifact name: vault_access"
        ),
        'hints': [
            {'text': 'Open the binary in a disassembler. Look for functions that compare your input to expected values. There are four of them — one per group.', 'cost': 35},
            {'text': 'One check uses arithmetic sums, one uses XOR masking, one uses additive rotation, one checks characters in reverse order. Solve each independently.', 'cost': 80},
        ],
        'connection_info': 'http://localhost:5016',
        'is_active': True,
    },
    {
        'title': 'Ghost Process',
        'category': 'rev',
        'difficulty': 'medium',
        'points': 300,
        'flag': 'CTF{4nt1_d3bug_byp4ss3d}',
        'description': (
            "Among the seized NIGHTFALL systems was a service called nightfall_daemon — "
            "a secure channel authenticator that was reportedly impossible to analyse.\n\n"
            "The daemon prints the channel credentials only after verifying the execution "
            "environment is clean. Any attempt to observe it directly causes it to terminate "
            "silently, leaving no trace.\n\n"
            "A defector's note recovered from the safe house reads:\n"
            "  'The daemon checks its environment three times before trusting it.\n"
            "   Each check is different. If any one fails, it dies.\n"
            "   But a dead program still has bones — and bones remember.'\n\n"
            "The flag is stored inside the binary in an obfuscated form.\n"
            "Find it without triggering the daemon's defenses.\n\n"
            "Retrieve the artifact from the NIGHTFALL terminal.\n"
            "The operation HMAC key is: nightfall_op_2024\n"
            "Artifact name: nightfall_daemon"
        ),
        'hints': [
            {'text': 'If the binary dies whenever you attach to it, try a different approach — you do not need to run it to understand it.', 'cost': 40},
            {'text': 'Look for a byte array in the binary and a loop that transforms each byte before the comparison. The transformation uses a single constant applied to every element.', 'cost': 90},
        ],
        'connection_info': 'http://localhost:5016',
        'is_active': True,
    },
    {
        'title': 'Compiled Confession',
        'category': 'rev',
        'difficulty': 'hard',
        'points': 400,
        'flag': 'CTF{pyc_byt3c0d3_d3c0mp1l3d}',
        'description': (
            "NIGHTFALL's logistics officer kept a personal archive of operation codes "
            "in an encrypted Python program. Before the arrest, the source code was deleted "
            "and only the compiled bytecode file survived on a seized USB drive.\n\n"
            "The file is named mission.pyc — a compiled Python module.\n\n"
            "When executed, it requests a passcode:\n"
            "  passcode:\n\n"
            "The correct passcode unlocks the operation code that was never meant to "
            "be recovered. The validation logic is obfuscated inside the bytecode.\n\n"
            "A handwritten note found with the USB drive says only:\n"
            "  '2 keys. 2 halves. Neither key is the flag.'\n\n"
            "Retrieve the artifact from the NIGHTFALL terminal.\n"
            "The operation HMAC key is: nightfall_op_2024\n"
            "Artifact name: mission.pyc"
        ),
        'hints': [
            {'text': 'Python bytecode can be turned back into source code. The tooling for this is publicly available — research Python decompilation.', 'cost': 50},
            {'text': 'Once you have the source, you will see two encrypted byte arrays and two keys. The decryption is symmetric — the same operation that encrypts will decrypt.', 'cost': 110},
        ],
        'connection_info': 'http://localhost:5016',
        'is_active': True,
    },
    {
        'title': 'The Interpreter',
        'category': 'rev',
        'difficulty': 'hard',
        'points': 500,
        'flag': 'CTF{vm_0pc0d3_r3v3}',
        'description': (
            "The most critical NIGHTFALL asset recovered was a binary called nightfall_vm.\n\n"
            "It is not a normal program. It contains its own interpreter — a miniature "
            "virtual machine with a custom instruction set that no standard disassembler "
            "understands.\n\n"
            "The VM runs an internal bytecode program that validates an input key. "
            "Standard reverse engineering approaches fail because the logic lives "
            "inside the bytecode, not the binary itself.\n\n"
            "The program prompts:\n"
            "  nightfall: key:\n\n"
            "A recovered technical memo states:\n"
            "  'The VM uses 8 opcodes. Input bytes are not compared directly.\n"
            "   They are transformed before comparison. The transformation is stateful —\n"
            "   each byte affects how the next is processed.\n"
            "   To recover the key, you must understand the transform and invert it.'\n\n"
            "Map the instruction set. Read the bytecode. Invert the transformation. "
            "Recover the key.\n\n"
            "Retrieve the artifact from the NIGHTFALL terminal.\n"
            "The operation HMAC key is: nightfall_op_2024\n"
            "Artifact name: nightfall_vm"
        ),
        'hints': [
            {'text': 'Find the exec() function in the binary. It is a loop with a switch-like structure. Each case number is an opcode — document what each one does to the stack and state.', 'cost': 80},
            {'text': 'The LOAD opcode does not push the raw input byte. It applies a transformation first — and that transformation updates a state variable used for the next byte. To reverse it, you need to run the same transform forward from the known initial state and XOR with the stored expected values.', 'cost': 160},
        ],
        'connection_info': 'http://localhost:5016',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed Reverse Engineering challenges (hardened, story-based)'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true')

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = Challenge.objects.filter(category='rev').delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} rev challenge(s).'))

        created = updated = 0
        for data in REV_CHALLENGES:
            raw_flag = data.pop('flag')
            ch, was_created = Challenge.objects.update_or_create(
                title=data['title'], defaults=data
            )
            ch.set_flag(raw_flag)
            ch.save()
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✔ Created : {ch.title} ({ch.points}pts)'))
            else:
                updated += 1
                self.stdout.write(f'  ↻ Updated : {ch.title} ({ch.points}pts)')

        self.stdout.write(self.style.SUCCESS(f'\nDone — {created} created, {updated} updated.'))
