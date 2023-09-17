from asgiref.sync import async_to_sync
from json import dumps, loads

from channels.generic.websocket import WebsocketConsumer

from .models import ROLES, Club, Player


class Consumer(WebsocketConsumer):
    """Socket consumer: handle and dispatch messages"""

    group = "asta"
    phase = "awaiting participants"
    clubs = set()
    roles = [r for r,_ in ROLES]
    club = r = player = None

    def connect(self):
        """Open web-socket connection"""
        group_add = async_to_sync(self.channel_layer.group_add)
        group_add(self.group, self.channel_name)
        self.accept()
        club = self.scope['user'].club.name
        self.clubs.add(club)
        group_send = async_to_sync(self.channel_layer.group_send)
        group_send(self.group, {'type': 'update.participants', 'new': club})

    def receive(self, text_data=None, bytes_data=None):
        """
        Get reecived data, dispatch them to correct handler and
        broadcast handler outpput
        """
        payload = loads(text_data)
        group_send = async_to_sync(self.channel_layer.group_send)
        event = payload['event']
        # Late join
        if event == 'late_join':
            data = payload
            data['type'] = 'late.join'
        # Synchronise (late joiner)
        if event == 'synchronise':
            data = payload
            data['type'] = 'synchronise'
        # Auction start / New-round start
        if event in ['start_auction', 'continue']:
            data = {'event': event, 'type': 'set.next.round'}
        # Start bid round
        elif event == 'start_bid':
            data = payload
            data['type'] = 'start.bid'
        # New bid received
        if event == 'new_bid':
            data = payload
            data['type'] = 'update.bid'
        # Assign player
        elif event == 'assign':
            data = {'event': 'continue', 'type': 'buy'}
        # Auction stop
        if event == 'stop_auction':
            data = payload
            data['type'] = 'stop.auction'
        # Dispatch
        group_send(self.group, data)

    def update_participants(self, data: dict) -> None:
        """Set participant list"""
        payload = {
            'event': 'join',
            'participants': list(self.clubs),
            'new': data['new'],
            'phase': self.phase
        }
        self.send(text_data=dumps(payload))

    def late_join(self, data: dict) -> None:
        """Send current state to late joiner"""
        if data['new'] != self.scope['user'].club.name:
            payload = {
                'event': 'late_join',
                'phase': self.phase,
                'participants': list(self.clubs),
                'club': self.club,
                'r': self.r,
                'role': self.roles[self.r],
                'player': self.player and self.player.id,
                'bidder': data['bidder'],
                'label': data['label']
            }
            if self.player is not None:
                payload['name'] = self.player.name
                payload['role'] = self.player.role
                payload['team'] = self.player.team
                payload['price'] = Player.object.get(id=self.player.id).price
                payload['amount'] = self.player.price
            self.send(text_data=dumps(payload))

    def synchronise(self, data: dict) -> None:
        """Synchronise late joiner"""
        self.phase = data['phase']
        self.clubs = set(data['participants'])
        self.club = data['club']
        self.r = data['r']
        self.player = data['player'] and Player.objects.get(id=data['player'])
        payload = {
            'event': 'synchronise', 'club': self.scope['user'].club.name
        }
        self.send(text_data=dumps(payload))

    def set_next_round(self, data: dict) -> None:
        """Launch next round"""
        payload = self._set_next_round()
        if 'event' in payload:  # auction ended!
            self.send(text_data=dumps(payload))
        else:
            payload['event'] = data['event']
            self.phase = "awaiting choice"
            self.send(text_data=dumps(payload))

    def start_bid(self, data: dict) -> None:
        """Select a new player and open bids"""
        club = Club.objects.get(name=self.club)
        self.player = Player.objects.get(id=data['player'])
        self.player.club = club
        payload = {
            'event': 'start_bid',
            'id': self.player.id,
            'name': self.player.name,
            'role': self.player.role,
            'team': self.player.team,
            'price': self.player.price,
            'club': self.club,
            'label': club.label
        }
        self.player.price = 1
        self.phase = "bids"
        self.send(text_data=dumps(payload))

    def update_bid(self, data: dict) -> None:
        """Update auction with last bid"""
        if data['amount'] > self.player.price:
            self.player.price = data['amount']
            self.player.club = Club.objects.get(name=data['club'])
            self.send(text_data=dumps(data))

    def buy(self, data: dict) -> None:
        """Assign player of current bid and continue"""
        self.player.save()
        payload = self._set_next_round()
        if 'event' in payload:  # auction ended!
            self.send(text_data=dumps(payload))
        else:
            payload['event'] = 'continue'
            payload['buyer'] = self.player.club.name
            payload['player'] = {
                'name': self.player.name,
                'team': self.player.team,
                'role': self.player.role,
                'price': self.player.price
            }
            payload['money'] = self.player.club.money
            self.phase = "awaiting choice"
            self.send(text_data=dumps(payload))

    def stop_auction(self, data: dict) -> None:
        """Pause auction saving current turn"""
        self.player = None
        club = Club.objects.get(name=self.club)
        club.next_call = self.roles[self.r]
        club.save()
        self.phase = "stopped"
        self.send(text_data=dumps(data))

    def disconnect(self, code):
        """Leave auction"""
        self.clubs.remove(self.scope['user'].club.name)
        group_discard = async_to_sync(self.channel_layer.group_discard)
        group_discard(self.group, self.channel_name)
        group_send = async_to_sync(self.channel_layer.group_send)
        group_send(self.group, {'type': 'update.participants'})

    def _set_next_round(self) -> dict:
        """Set caller club and to-call role for next turn"""
        clubs_names = sorted(list(self.clubs))
        clubs = Club.objects.filter(name__in=clubs_names)
        if self.phase == 'awaiting participants':  # first auction turn: init.
            club = (clubs.filter(next_call__isnull=False) or clubs).first()
            self.club = club.name
            role = club.next_call or 'P'
            self.r = self.roles.index(role)
        elif self.phase != 'stopped':
            # Determines next caller taking into account if roster is
            # already full for the given role
            cannot_call = True
            # Set check condition to avoid infinite loop
            club_0 = self.club
            r_0 = self.r
            while cannot_call:
                self.r = (self.r + 1) % 4
                if self.r == 0:
                    c = (clubs_names.index(self.club) + 1) % len(clubs_names)
                    self.club = clubs_names[c]
                role = self.roles[self.r]
                cannot_call = clubs.get(name=self.club).is_full(role)
                if cannot_call and self.club == club_0 and self.r == r_0:
                    return {'event': 'end'}
        return {'club': self.club, 'role': role}