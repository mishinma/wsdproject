from django.shortcuts import render
from community.models import Game, Game_Category


def index(request):
    top_games = Game.objects.all().order_by('-rating')
    return render(request, "base/index.html", {'top_games': top_games})
