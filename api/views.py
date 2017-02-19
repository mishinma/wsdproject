from community.models import GameCategory, Game, GameScore
from accounts.models import UserMethods
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


def get_games_of_category(request, category):
    try:
        category = GameCategory.objects.filter(name__iexact=category)
    except GameCategory.DoesNotExist:
        message = json.dumps({'error': 404, 'message': 'category does not exist'})
        return HttpResponseNotFound(message, 'application/json')
    games = Game.objects.filter(category=category).values('id', 'name', 'developer', 'price')
    data = json.dumps([game for game in games], cls=DjangoJSONEncoder)
    if 'callback' in request.GET:
        data = '%s(%s)' % (request.GET['callback'], data)
        return HttpResponse(data, 'text/javascript')
    else:
        return HttpResponse(data, 'application/json')


def get_games_of_dev(request, dev_id):
    try:
        dev = UserMethods.objects.get(id=dev_id)
    except UserMethods.DoesNotExist:
        message = json.dumps({'error': 404, 'message': 'developer does not exist'})
        return HttpResponseNotFound(message, 'application/json')

    if not dev.is_developer():
        message = json.dumps({'error': 400, 'message': 'not a developer'})
        return HttpResponseBadRequest(message, 'application/json')
    games = Game.objects.filter(developer=dev).values('id', 'name', 'category', 'price')
    data = json.dumps([game for game in games], cls=DjangoJSONEncoder)
    if 'callback' in request.GET:
        data = '%s(%s)' % (request.GET['callback'], data)
        return HttpResponse(data, 'text/javascript')
    else:
        return HttpResponse(data, 'application/json')


def get_game_detail(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        message = json.dumps({'error': 404, 'message': 'game does not exist'})
        return HttpResponseNotFound(message, 'application/json')
    data = json.dumps({
        'name': game.name,
        'description': game.description,
        'developer_id': game.developer.id,
        'developer_name': game.developer.username,
        'category_id': game.category.id,
        'category_name': game.category.name,
        'price': game.price,
        'sales_price': game.sales_price
        }, cls=DjangoJSONEncoder)
    if 'callback' in request.GET:
        data = '%s(%s)' % (request.GET['callback'], data)
        return HttpResponse(data, 'text/javascript')
    else:
        return HttpResponse(data, 'application/json')


def get_scores_of_game(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        message = json.dumps({'error': 404, 'message': 'game does not exist'})
        return HttpResponseNotFound(message, 'application/json')
    scores = GameScore.objects.filter(game=game).values('player', 'player__username', 'score', 'timestamp')

    data = json.dumps([score for score in scores], cls=DjangoJSONEncoder)
    if 'callback' in request.GET:
        data = '%s(%s)' % (request.GET['callback'], data)
        return HttpResponse(data, 'text/javascript')
    else:
        return HttpResponse(data, 'application/json')


def get_categories(request):
    categories = GameCategory.objects.all().values('id', 'name')
    data = json.dumps([cat for cat in categories], cls=DjangoJSONEncoder)
    if 'callback' in request.GET:
        data = '%s(%s)' % (request.GET['callback'], data)
        return HttpResponse(data, 'text/javascript')
    else:
        return HttpResponse(data, 'application/json')


def get_developers(request):
    devs = UserMethods.objects.filter(groups__name='developer').values('id', 'username')
    data = json.dumps([dev for dev in devs], cls=DjangoJSONEncoder)
    if 'callback' in request.GET:
        data = '%s(%s)' % (request.GET['callback'], data)
        return HttpResponse(data, 'text/javascript')
    else:
        return HttpResponse(data, 'application/json')
