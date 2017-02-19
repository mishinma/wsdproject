from django.shortcuts import render
from community.models import Game


def index(request):
    games = Game.objects.all()
    games= Game.objects.add_action(games, request.user)
    return render(request, "base/index.html", {'top_games': games})
