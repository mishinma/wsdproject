from django.contrib.auth.models import Group


def add_to_players(backend, user, response, *args, **kwargs):
    if user.is_authenticated():
        player = Group.objects.get(name='player')
        user.groups.add(player)
