from django.contrib.auth.models import AbstractUser
from django.db import models


class Player(AbstractUser):
    """Individual CTF participant — no teams."""
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    country = models.CharField(max_length=64, blank=True)
    website = models.URLField(blank=True)
    affiliation = models.CharField(max_length=128, blank=True, help_text="University, company, etc.")
    score = models.IntegerField(default=0)
    last_solve_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-score', 'last_solve_time']

    def __str__(self):
        return self.username

    @property
    def rank(self):
        """Live rank among all players."""
        from django.db.models import F
        higher = Player.objects.filter(
            score__gt=self.score
        ).count()
        return higher + 1

    @property
    def solves_count(self):
        return self.submissions.filter(is_correct=True).count()
