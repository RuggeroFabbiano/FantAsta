# from django.contrib.auth.models import User
# from django.db.models import (CASCADE, SET_NULL, CharField, ForeignKey, Model,
#                               OneToOneField, PositiveIntegerField)


# ROLES = [
#     ('P', 'portiere'),
#     ('D', 'difensore'),
#     ('C', 'centrocampista'),
#     ('A', 'attaccante')
# ]


# class Club(Model):
#     """Teams participating to the ligue"""

#     name = CharField(max_length=50)
#     money = PositiveIntegerField(default=500)
#     next_call = CharField(max_length=1, choices=ROLES, null=True)
#     user = OneToOneField(User, CASCADE)

#     class Meta:
#         ordering = ['name']

#     def __str__(self):
#         return self.name

#     @property
#     def label(self):
#         """
#         Associate to the team an anonymised label indexed by
#         alphabetical order
#         """
#         return F"team{Club.objects.filter(name__lte=self.name).count()}"


# class Player(Model):
#     """Serie A football players"""

#     name = CharField(max_length=50)
#     team = CharField(max_length=50)
#     role = CharField(max_length=1, choices=ROLES)
#     price = PositiveIntegerField()
#     club = ForeignKey(Club, SET_NULL, "players", null=True)

#     class Meta:
#         ordering = ['name']

#     def __str__(self):
#         return F"{self.name} ({self.team})"