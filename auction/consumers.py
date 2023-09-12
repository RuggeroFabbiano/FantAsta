from asgiref.sync import async_to_sync
from json import dumps, loads

from channels.generic.websocket import WebsocketConsumer

from .models import ROLES, Club, Player


class Consumer(WebsocketConsumer):
    """Socket consumer: handle and dispatch messages"""

    group = 'asta'
    participants = []
    phase = 'awaiting participants'
    clubs = list(Club.objects.values_list('name', flat=True))
    roles = [r for r,_ in ROLES]
    c = r = None
    player = None

    def connect(self):
        """Open web-socket connection"""
        group_add = async_to_sync(self.channel_layer.group_add)
        group_add(self.group, self.channel_name)
        self.accept()
        self.participants.append(self.scope['user'].username)
        group_send = async_to_sync(self.channel_layer.group_send)
        group_send(self.group, {'type': 'update.participants'})

    def receive(self, text_data=None, bytes_data=None):
        """
        Get reecived data, dispatch them to correct handler and
        broadcast handler outpput
        """
        payload = loads(text_data)
        group_send = async_to_sync(self.channel_layer.group_send)
        event = payload['event']
        # Auction start / New-round start
        if event in ['start_auction', 'continue']:
            data = {'event': event, 'type': 'set.next.round'}
        # Start bid round
        elif event == 'start_bid':
            data = payload
            data['type'] = 'start.bid'
        # New bid received / auction stop
        if event in ['new_bid', 'stop_auction']:
            data = payload
            data['type'] = 'broadcast'
        # Assign player
        elif event == 'buy':
            self._buy_player(payload)
            self._set_next_turn()
            data = {'event': 'continue', 'type': 'set.next.round'}
        # Dispatch
        group_send(self.group, data)

    def update_participants(self, data: dict) -> None:
        """Set participant list"""
        payload = {
            'event': 'join',
            'participants': self.participants,
            'total': len(self.clubs),
            'phase': self.phase
        }
        self.send(text_data=dumps(payload))

    def set_next_round(self, data: dict) -> None:
        """Launch next round"""
        self._set_next_round()
        self.phase = "awaiting choice"
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
            'id': self.player.id,
            'name': self.player.name,
            'role': self.player.role,
            'team': self.player.team,
            'price': self.player.price,
            'club': self.clubs[self.c],
            'label': F'team{self.c + 1}'
        }
        self.send(text_data=dumps(payload))

    def broadcast(self, data: dict) -> None:
        """Broadcast message as-is"""
        self.send(text_data=dumps(data))

    def buy(self, data: dict) -> None:
        """Assign player of current bid"""
        self.send(text_data=dumps(data))

    def disconnect(self, code):
        """Leave auction"""
        self.participants.remove(self.scope['user'].username)
        group_send = async_to_sync(self.channel_layer.group_send)
        group_send(self.group, {'type': 'update.participants'})
        group_discard = async_to_sync(self.channel_layer.group_discard)
        group_discard(self.group, self.channel_name)

    def _set_next_round(self) -> None:
        """Set caller club and to-call role for next turn"""
        if self.c is None:  # first auction turn: init.
            clubs = Club.objects
            club = clubs.filter(next_call__isnull=False) or clubs.first()
            self.c = self.clubs.index(club.name)
            self.r = self.roles.index(club.next_call or 'P')
        else:
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