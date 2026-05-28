from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player


@admin.register(Player)
class PlayerAdmin(UserAdmin):
    list_display = ('username', 'email', 'score', 'solves_count', 'country', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'country')
    search_fields = ('username', 'email', 'affiliation')
    ordering = ('-score',)
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = UserAdmin.fieldsets + (
        ('CTF Profile', {
            'fields': ('bio', 'avatar', 'country', 'website', 'affiliation', 'score', 'last_solve_time')
        }),
    )

    def solves_count(self, obj):
        return obj.solves_count
    solves_count.short_description = 'Solves'
