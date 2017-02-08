from django.shortcuts import render
from django.http import HttpResponse
from .models import Developer, Category, Game, Player, Game_Score, Game_State
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


def index(request):
    return render(request, "community/index.html")
    # return HttpResponse("Hello World!")


def game_info(request):
    return render(request, "community/game-info.html")
