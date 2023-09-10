from asgiref.sync import async_to_sync
from json import dumps, loads

from channels.generic.websocket import WebsocketConsumer

from .models import ROLES, Club, Player


class Consumer(WebsocketConsumer):
    """Socket consumer: handle and dispatch messages"""

    group = 'asta'
    clubs = list(Club.objects.values_list('name', flat=True))
    roles = [r for r,_ in ROLES]
    c = r = None
    player = None

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
        payload = loads(text_data)
        group_send = async_to_sync(self.channel_layer.group_send)
        event = payload['event']
        # Join acution, new bid received, auction stop
        if event in ['join', 'new_bid', 'stop_auction']:
            data = payload
            data['type'] = 'broadcast'
        # Auction start
        elif event == 'start_auction':
            self._set_first_turn()
            data = {'event': 'start_auction', 'type': 'set.next.round'}
        # New-turn start
        elif event == 'continue':
            self._set_next_turn()
            data = {'event': 'continue', 'type': 'set.next.round'}
        # Start bid round
        elif event == 'start_bid':
            data = payload
            data['type'] = 'start.bid'
        # Assign player
        elif event == 'buy':
            self._buy_player(payload)
            self._set_next_turn()
            data = {'event': 'continue', 'type': 'set.next.round'}
        # Dispatch
        group_send(self.group, data)

    def broadcast(self, data: dict) -> None:
        """Broadcast message as-is"""
        del data['type']
        self.send(text_data=dumps(data))

    def set_next_round(self, data: dict) -> None:
        """Launch next round"""
        payload = {
            'event': data['event'],
            'club': self.clubs[self.c],
            'role': self.roles[self.r]
        }
        self.send(text_data=dumps(payload))

    def start_bid(self, data: dict) -> None:
        """Select a new player and open bids"""
        self.player = Player.objects.get(id=data['player'])
        payload = {
            'club': self.clubs[self.c],
            'player_name': self.player.name,
            'player_team': self.player.team,
            'player_role': self.player.role
        }
        self.send(text_data=dumps(payload))

    def buy(self, data: dict) -> None:
        """Assign player of current bid"""
        self.send(text_data=dumps(data))

    def disconnect(self, code):
        """Leave auction"""
        group_discard = async_to_sync(self.channel_layer.group_discard)
        group_discard(self.group, self.channel_name)

    def _set_first_turn(self) -> None:
        """Set starting turn"""
        clubs = Club.objects
        club = clubs.filter(next_call__isnull=False) or clubs.first()
        self.c = self.clubs.index(club.name)
        self.r = self.roles.index(club.next_call or 'P')

    def _set_next_turn(self) -> None:
        """Set next turn"""
        self.r = (self.r + 1) % 4
        if self.r == 0:
            self.c = (self.c + 1) % len(self.clubs)

    def _buy_player(self, data: dict) -> None:
        """Buy player of current bid"""
        club = Club.objects.get(name=data['club'])
        club.money -= data['value']
        club.save()
        self.player.club = club
        self.player.save()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=dumps({"message": message}))