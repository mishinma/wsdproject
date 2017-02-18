from django.shortcuts import render
from community.models import Game


def index(request):
    top_games = Game.objects.order_by('-rating')
    top_games= Game.objects.add_action(top_games, request.user)
    return render(request, "base/index.html", {'top_games': top_games})
