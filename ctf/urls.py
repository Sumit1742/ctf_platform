from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from ctf.context_processors import CATEGORY_META
from ctf.apps.challenges.models import Challenge, CATEGORY_CHOICES
from ctf.apps.submissions.models import Submission


def home(request):
    all_categories = {}
    if request.user.is_authenticated:
        solved_ids = set(
            Submission.objects.filter(player=request.user, is_correct=True)
            .values_list('challenge_id', flat=True)
        )
        challenges = Challenge.objects.filter(is_active=True)
        for cat_key, cat_label in CATEGORY_CHOICES:
            cat_chs = list(challenges.filter(category=cat_key))
            if cat_chs:
                meta = CATEGORY_META.get(cat_key, {})
                all_categories[cat_label] = {
                    'key':         cat_key,
                    'color':       meta.get('color', '#888'),
                    'icon':        meta.get('icon', ''),
                    'description': meta.get('description', ''),
                    'solved':      sum(1 for c in cat_chs if c.id in solved_ids),
                    'total':       len(cat_chs),
                }
    return render(request, 'home.html', {'all_categories': all_categories})


def about(request):
    rules = [
        "Do not attack the CTF platform infrastructure itself.",
        "Do not share flags or solutions with other players.",
        "Do not brute-force the flag submission endpoint.",
        "Each challenge runs in its own isolated Docker container.",
        "If a challenge is broken, report it — do not exploit the break.",
        "Have fun and learn something new.",
    ]
    return render(request, 'about.html', {
        'categories_meta': list(CATEGORY_META.items()),
        'rules': rules,
    })


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('accounts/', include('ctf.apps.accounts.urls')),
    path('challenges/', include('ctf.apps.challenges.urls')),
    path('scoreboard/', include('ctf.apps.scoreboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
