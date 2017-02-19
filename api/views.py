from community.models import GameCategory, Game
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
import simplejson as json
import decimal


def get_games_of_category(request, category):
    try:
        category = GameCategory.objects.filter(name__iexact=category)
    except GameCategory.DoesNotExist:
        return HttpResponseNotFound
    games = Game.objects.filter(category=category).values('name', 'developer__username', 'price')

    data = [game for game in games]
    if 'callback' in request.GET:
        data = '%s(%s)' % (request.GET['callback'], data)
        return HttpResponse(data, 'text/javascript')
    else:
        return HttpResponse(json.dumps(data, use_decimal=True), 'application/json')


def get_games_of_dev(request, dev_id):
    pass


def get_game_detail(request, game_id):
    pass


def get_scores_of_game(request):
    pass
