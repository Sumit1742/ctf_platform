from django.db import models
from django.conf import settings
import hashlib


CATEGORY_CHOICES = [
    ('web',       'Web'),
    ('crypto',    'Cryptography'),
    ('osint',     'OSINT'),
    ('forensics', 'Forensics'),
    ('pwn',       'Binary / Pwn'),
    ('misc',      'Miscellaneous'),
    ('rev',       'Reverse Engineering'),
]

DIFFICULTY_CHOICES = [
    ('easy',   'Easy'),
    ('medium', 'Medium'),
    ('hard',   'Hard'),
]

CATEGORY_COLORS = {
    'web':       '#378ADD',
    'crypto':    '#7F77DD',
    'osint':     '#1D9E75',
    'forensics': '#BA7517',
    'pwn':       '#E24B4A',
    'misc':      '#888780',
    'rev':       '#D4537E',
}


class Challenge(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    points = models.IntegerField(default=100)
    flag_hash = models.CharField(max_length=64, help_text="SHA-256 hash of the flag")

    # Files & connections
    files = models.ManyToManyField('ChallengeFile', blank=True, related_name='challenges')
    connection_info = models.CharField(
        max_length=300, blank=True,
        help_text="e.g. nc challenge 4444  OR  http://challenge:5000"
    )

    # Docker
    docker_image = models.CharField(max_length=200, blank=True)
    docker_port = models.IntegerField(null=True, blank=True)

    # Visibility & ordering
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=0, help_text="0 = unlimited")

    # Hints (stored as JSON list of dicts {text, cost})
    hints = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'points', 'order']

    def __str__(self):
        return f"[{self.category}] {self.title} ({self.points}pts)"

    def set_flag(self, raw_flag: str):
        """Hash and store the flag. Call this instead of setting flag_hash directly."""
        self.flag_hash = hashlib.sha256(raw_flag.strip().encode()).hexdigest()

    def check_flag(self, submitted: str) -> bool:
        submitted_hash = hashlib.sha256(submitted.strip().encode()).hexdigest()
        return submitted_hash == self.flag_hash

    @property
    def solves_count(self):
        return self.submissions.filter(is_correct=True).count()

    @property
    def color(self):
        return CATEGORY_COLORS.get(self.category, '#888780')

    def is_solved_by(self, user) -> bool:
        return self.submissions.filter(player=user, is_correct=True).exists()


class ChallengeFile(models.Model):
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE,
        related_name='attached_files', null=True, blank=True
    )
    file = models.FileField(upload_to='challenge_files/')
    display_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name
