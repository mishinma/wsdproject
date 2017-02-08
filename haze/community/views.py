from django.shortcuts import render


def index(request):
    return render(request, "community/index.html")
    # return HttpResponse("Hello World!")


def game_info(request, id):
    return render(request, "community/game-info.html", {'id': id})
