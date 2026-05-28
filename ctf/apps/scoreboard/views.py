from django.shortcuts import render
from django.http import JsonResponse
from ctf.apps.accounts.models import Player
from ctf.apps.submissions.models import Submission
from django.db.models import Count, Max


def scoreboard_view(request):
    players = Player.objects.filter(
        is_active=True, is_staff=False
    ).order_by('-score', 'last_solve_time')[:100]

    return render(request, 'scoreboard/scoreboard.html', {
        'players': players,
        'current_user': request.user if request.user.is_authenticated else None,
    })


def scoreboard_api(request):
    """JSON endpoint polled by the live scoreboard widget."""
    players = Player.objects.filter(
        is_active=True, is_staff=False
    ).order_by('-score', 'last_solve_time').values(
        'username', 'score', 'last_solve_time', 'country', 'affiliation'
    )[:100]

    data = []
    for i, p in enumerate(players, 1):
        data.append({
            'rank': i,
            'username': p['username'],
            'score': p['score'],
            'country': p['country'],
            'affiliation': p['affiliation'],
            'last_solve': p['last_solve_time'].isoformat() if p['last_solve_time'] else None,
        })

    return JsonResponse({'players': data})
