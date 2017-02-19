from community.models import GameCategory, Game
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
import simplejson as json
import decimal


def get_games_of_category(request, category):
    try:
        category = GameCategory.objects.filter(name__iexact=category)
    except GameCategory.DoesNotExist:
        return HttpResponseNotFound
    games = Game.objects.filter(category=category).values('name', 'developer', 'price')

    data = [game for game in games]

    return HttpResponse(json.dumps(data, use_decimal=True), 'application/json')


def get_games_of_dev(request, dev_id):
    pass


def get_game_detail(request, game_id):
    pass


def get_scores_of_game(request):
    pass


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)
