from django.shortcuts import render, get_object_or_404
from .models import Game


def index(request):
    return render(request, "community/index.html")


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})


def welcome_user(request):
    user = request.user
    return render(request, "community/welcome_user.html", {'user': user})
