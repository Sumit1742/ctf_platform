from django.conf import settings

CATEGORY_META = {
    'web':       {'icon': '🌐', 'color': '#38bdf8', 'label': 'Web',              'description': 'XSS, SQLi, SSTI, JWT attacks and web vulnerabilities.'},
    'crypto':    {'icon': '🔐', 'color': '#a78bfa', 'label': 'Cryptography',     'description': 'Break ciphers, crack hashes, and decode secret messages.'},
    'osint':     {'icon': '🔍', 'color': '#00ff9d', 'label': 'OSINT',            'description': 'Open-source intelligence gathering and digital footprinting.'},
    'forensics': {'icon': '🧬', 'color': '#fbbf24', 'label': 'Forensics',        'description': 'Analyse files, memory dumps, and hidden data in artifacts.'},
    'pwn':       {'icon': '💥', 'color': '#f87171', 'label': 'Binary / Pwn',     'description': 'Buffer overflows, ROP chains, and binary exploitation.'},
    'rev':       {'icon': '⚙️',  'color': '#f472b6', 'label': 'Reverse Engineering','description': 'Disassemble binaries and reverse-engineer compiled code.'},
    'misc':      {'icon': '🎲', 'color': '#64748b', 'label': 'Miscellaneous',    'description': 'Puzzles that do not fit neatly into another category.'},
}


def ctf_settings(request):
    nav_categories = [
        (key, meta['label'], meta['color'])
        for key, meta in CATEGORY_META.items()
    ]
    return {
        'CTF_NAME': settings.CTF_NAME,
        'CTF_START': settings.CTF_START,
        'CTF_END': settings.CTF_END,
        'nav_categories': nav_categories,
    }
