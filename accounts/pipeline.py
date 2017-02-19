from django.contrib.auth.models import Group
from accounts.models import EmailConfirmed


def add_to_players(backend, user, response, *args, **kwargs):
    if user.is_authenticated() and not user.groups.exists():
        player = Group.objects.get(name='player')
        user.groups.add(player)


def add_email_confirmed(backend, user, response, *args, **kwargs):
    if user.is_authenticated() and not EmailConfirmed.objects.filter(user=user).exists():
        EmailConfirmed.objects.create(user=user)
