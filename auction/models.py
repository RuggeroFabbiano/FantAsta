from django.contrib.auth.models import User
from django.db.models import (CASCADE, SET_NULL, CharField, ForeignKey, Model,
                              OneToOneField, PositiveIntegerField, QuerySet,
                              Sum)


ROLES = [
    ('P', 'portiere'),
    ('D', 'difensore'),
    ('C', 'centrocampista'),
    ('A', 'attaccante')
]


class Club(Model):
    """Teams participating to the ligue"""

    name = CharField(max_length=50)
    next_call = CharField(max_length=1, choices=ROLES, null=True)
    user = OneToOneField(User, CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def money(self) -> int:
        """Money left to the club"""
        money_spent = self.players.aggregate(Sum('price'))['price__sum'] or 0
        return 500 - money_spent

    @property
    def label(self):
        """
        Associate to the team an anonymised label indexed by
        alphabetical order
        """
        return F"team{Club.objects.filter(name__lte=self.name).count()}"

    @property
    def n_p(self) -> int:
        """Count of goalkeepers"""
        return self.players.filter(role='P').count()

    @property
    def n_d(self) -> int:
        """Count of defenders"""
        return self.players.filter(role='D').count()

    @property
    def n_c(self) -> int:
        """Count of midfielders"""
        return self.players.filter(role='C').count()

    @property
    def n_a(self) -> int:
        """Count of strikers"""
        return self.players.filter(role='A').count()

    def is_full(self, role: str) -> bool:
        """Tell if club is full for a given role"""
        max_allowed = {'P': 3, 'D': 8, 'C': 8, 'A': 6}[role]
        return self.players.filter(role=role).count() == max_allowed


class Player(Model):
    """Serie A football players"""

    name = CharField(max_length=50)
    team = CharField(max_length=50)
    role = CharField(max_length=1, choices=ROLES)
    price = PositiveIntegerField()
    club = ForeignKey(Club, SET_NULL, "players", null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return F"{self.name} ({self.team})"