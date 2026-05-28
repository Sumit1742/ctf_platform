from django.db import models
from django.conf import settings


class Submission(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    challenge = models.ForeignKey(
        'challenges.Challenge',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    submitted_flag = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        # Prevent duplicate correct solves
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'challenge'],
                condition=models.Q(is_correct=True),
                name='unique_correct_solve_per_player'
            )
        ]

    def __str__(self):
        status = '✓' if self.is_correct else '✗'
        return f"{status} {self.player.username} → {self.challenge.title}"
