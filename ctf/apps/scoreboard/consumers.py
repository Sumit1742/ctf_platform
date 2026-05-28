import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ScoreboardConsumer(AsyncWebsocketConsumer):
    GROUP = 'scoreboard'

    async def connect(self):
        await self.channel_layer.group_add(self.GROUP, self.channel_name)
        await self.accept()
        # Send current state immediately on connect
        players = await self.get_scoreboard()
        await self.send(text_data=json.dumps({'type': 'init', 'players': players}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP, self.channel_name)

    async def scoreboard_update(self, event):
        """Called by broadcast_scoreboard_update task."""
        await self.send(text_data=json.dumps({
            'type': 'update',
            'players': event['players'],
        }))

    @database_sync_to_async
    def get_scoreboard(self):
        from ctf.apps.accounts.models import Player
        players = Player.objects.filter(
            is_active=True, is_staff=False
        ).order_by('-score', 'last_solve_time').values(
            'username', 'score', 'country', 'last_solve_time'
        )[:100]

        result = []
        for i, p in enumerate(players, 1):
            result.append({
                'rank': i,
                'username': p['username'],
                'score': p['score'],
                'country': p['country'] or '',
                'last_solve': p['last_solve_time'].isoformat() if p['last_solve_time'] else None,
            })
        return result
