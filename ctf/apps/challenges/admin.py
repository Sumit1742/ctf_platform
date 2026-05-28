from django.contrib import admin
from .models import Challenge, ChallengeFile


class ChallengeFileInline(admin.TabularInline):
    model = ChallengeFile
    extra = 1
    fields = ('display_name', 'file')


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'points', 'is_active', 'solves_count')
    list_filter = ('category', 'difficulty', 'is_active')
    list_editable = ('is_active', 'points')
    search_fields = ('title', 'description')
    inlines = [ChallengeFileInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'category', 'difficulty', 'points', 'is_active', 'order')
        }),
        ('Flag', {
            'fields': ('flag_hash',),
            'description': 'Use the set_flag() method or management command to set the flag safely.'
        }),
        ('Connection / Docker', {
            'fields': ('connection_info', 'docker_image', 'docker_port'),
            'classes': ('collapse',)
        }),
        ('Game Mechanics', {
            'fields': ('max_attempts', 'hints'),
            'classes': ('collapse',)
        }),
    )

    def solves_count(self, obj):
        return obj.solves_count
    solves_count.short_description = 'Solves'
