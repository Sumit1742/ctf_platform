from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@shared_task
def broadcast_scoreboard_update():
    from ctf.apps.accounts.models import Player
    channel_layer = get_channel_layer()

    players = Player.objects.filter(
        is_active=True, is_staff=False
    ).order_by('-score', 'last_solve_time').values(
        'username', 'score', 'country', 'last_solve_time'
    )[:100]

    data = []
    for i, p in enumerate(players, 1):
        data.append({
            'rank': i,
            'username': p['username'],
            'score': p['score'],
            'country': p['country'] or '',
            'last_solve': p['last_solve_time'].isoformat() if p['last_solve_time'] else None,
        })

    async_to_sync(channel_layer.group_send)(
        'scoreboard',
        {'type': 'scoreboard.update', 'players': data}
    )
