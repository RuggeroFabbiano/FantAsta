from asgiref.sync import async_to_sync
from json import dumps, loads

from channels.generic.websocket import WebsocketConsumer

# from .models import ROLES, Club, Player


class Consumer(WebsocketConsumer):
    """Socket consumer: handle and dispatch messages"""

    group = 'asta'
    # clubs = list(Club.objects.values_list('name', flat=True))
    # roles = [r for r,_ in ROLES]

    def connect(self):
        """Open web-socket connection"""
        group_add = async_to_sync(self.channel_layer.group_add)
        group_add(self.group, self.channel_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        """
        Get reecived data, dispatch them to correct handler and
        broadcast handler outpput
        """
        data = loads(text_data)
        group_send = async_to_sync(self.channel_layer.group_send)
        if data['event'] == 'join':
            payload = data
            payload['type'] = 'join.confirmation'
        # elif data['event'] == 'start_auction':
        #     self.set_first_turn()
        #     payload = {'event': 'start_auction', 'type': 'next.round'}
        # elif data['event'] == 'continue':
        #     self.set_next_turn()
        #     payload = {'event': 'continue', 'type': 'next.round'}
        # elif data['event'] == 'start_bid':
        #     payload = {'type': 'start.bid', 'player': data['player']}
        # elif data['event'] == 'new_bid':
        #     payload = data
        #     payload['type'] = 'new.bid'
        # elif data['event'] == 'buy':
        #     self.buy_player(data)
        #     self.set_next_turn()
        #     payload = {'event': 'continue', 'type': 'next.round'}
        # elif data['event'] == 'stop_auction':
        #     payload = data
        #     payload['type'] = 'stop.auction'
        group_send(self.group, payload)

    def join_confirmation(self, data: dict) -> None:
        """Send join confirmation"""
        del data['type']
        self.send(text_data=dumps(data))

    # def next_round(self, data: dict) -> None:
    #     """Launch next round"""
    #     payload = {'event': data['event'], 'club': self.clubs[self.c], 'role': self.roles[self.r]}
    #     self.send(text_data=dumps(payload))

    # def start_bid(self, data: dict) -> None:
    #     """Select a new player and open bids"""
    #     self.player = Player.objects.get(id=data['player'])
    #     payload = {
    #         'club': self.clubs[self.c],
    #         'player_name': self.player.name,
    #         'player_team': self.player.team,
    #         'player_role': self.player.role
    #     }
    #     self.send(text_data=dumps(payload))

    # def new_bid(self, data: dict) -> None:
    #     """Make a new bid on current player"""
    #     del data['type']
    #     self.send(text_data=dumps(data))

    # def buy(self, data: dict) -> None:
    #     """Buy player of current bid"""
    #     club = Club.objects.get(name=data['club'])
    #     club.money -= data['value']
    #     club.save()
    #     self.player.club = club
    #     self.player.save()
    #     self.send(text_data=dumps(data))

    # def stop_auction(self, data: dict) -> None:
    #     """Stop auction"""
    #     del data['type']
    #     self.send(text_data=dumps(data))

    def disconnect(self, close_code):
        """Leave auction"""
        group_discard = async_to_sync(self.channel_layer.group_discard)
        group_discard(self.group, self.channel_name)

    # def set_first_turn(self) -> None:
    #     """Set starting turn"""
    #     club = (
    #         Club.objects.filter(next_call__isnull=False) or Club.objects
    #     ).first()
    #     self.c = self.clubs.index(club.name)
    #     self.r = self.roles.index(club.next_call or 'P')

    # def set_next_turn(self) -> None:
    #     """Set next turn"""
    #     self.r = (self.r + 1) % 4
    #     if self.r == 0:
    #         self.c = (self.c + 1) % len(self.clubs)

    # def buy_player(self, data: dict) -> None:
    #     """Buy player of current bid"""
    #     club = Club.objects.get(name=data['club'])
    #     club.money -= data['value']
    #     club.save()
    #     self.player.club = club
    #     self.player.save()