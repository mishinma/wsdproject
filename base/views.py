from django.shortcuts import render
from community.models import Game, Game_Category


def index(request):
    games = Game.objects.all().
    return render(request, "base/index.html", {'games': games})
