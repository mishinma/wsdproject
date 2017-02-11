from django.shortcuts import render, get_object_or_404
from .models import Game


def index(request):
    return render(request, "community/index.html")
    # return HttpResponse("Hello World!")


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})
