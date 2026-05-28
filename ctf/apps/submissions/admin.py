from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('player', 'challenge', 'is_correct', 'submitted_at', 'ip_address')
    list_filter = ('is_correct', 'challenge__category')
    search_fields = ('player__username', 'challenge__title', 'submitted_flag')
    readonly_fields = ('submitted_at', 'ip_address')
    date_hierarchy = 'submitted_at'
