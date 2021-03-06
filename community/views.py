import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, permission_required, PermissionDenied
from community.models import Game, GameScore, GameState, GameCategory, \
    ACTION_BUY, ACTION_DEVELOP, ACTION_PLAY
from community.forms import GameForm
from webshop.models import Purchase
from django.views import defaults


MESSAGE_TYPE_SCORE = 'SCORE'
MESSAGE_TYPE_SAVE = 'SAVE'
MESSAGE_TYPE_LOAD_REQUEST = 'LOAD_REQUEST'
MESSAGE_TYPE_LOAD = 'LOAD'
MESSAGE_TYPE_ERROR = 'ERROR'
MESSAGE_TYPE_SETTING = 'SETTING'

MESSAGE_SAVE_SCORE_ERROR = "Sorry, we couldn't save your score."
MESSAGE_SAVE_STATE_ERROR = "Sorry, we couldn't save your state."
MESSAGE_LOAD_GAME_ERROR = "Sorry, we couldn't load your game."

CHART_ALL_GAMES_SOLD_MONTH = 'allGamesSoldMonth'
CHART_REVENUE_PER_GAME = 'allRevenuePerGame'


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game = Game.objects.add_action_single(game, request.user)

    if request.is_ajax() and game.action == ACTION_DEVELOP:
        return get_statistics_game_info(request, game=game)

    context = {
        'game': game,
    }
    return render(request, "community/game-info.html", context=context)


@login_required
@permission_required('community.play_game', raise_exception=True)
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Redirect if the user hasn't purchased the game
    if not request.user.plays_game(game):
        return redirect('webshop:purchase-game', game_id=game_id)

    if request.is_ajax():
        message_type = request.POST.get("messageType")

        if message_type == MESSAGE_TYPE_SCORE:
            action_func = save_score
        elif message_type == MESSAGE_TYPE_SAVE:
            action_func = save_state
        elif message_type == MESSAGE_TYPE_LOAD_REQUEST:
            action_func = load_game
        else:
            return HttpResponseBadRequest()

        return action_func(request, game)

    # TODO: add top scores
    context = {
        'game': game,
        'user_high_score': game.get_user_high_score(request.user),
        'user_last_score': game.get_user_last_score(request.user),
        'top_scores': game.get_top_scores(5)
    }

    return render(request, "community/game-play.html", context)


@never_cache
def save_score(request, game):
    """ Save game score from the received postMessage """

    try:
        score_value = request.POST["score"]
    except KeyError:
        return HttpResponseBadRequest(MESSAGE_SAVE_SCORE_ERROR)

    GameScore.objects.create(
        score=score_value, game=game, player=request.user)

    # Fetch the scores and update them
    user_high_score = game.get_user_high_score(request.user)
    user_last_score = game.get_user_last_score(request.user)
    top_scores = [[score.player.username, score.score] for score in game.get_top_scores(5)]

    return JsonResponse({
        'userHighScore': user_high_score,
        'userLastScore': user_last_score,
        'topScores': top_scores
    })


@never_cache
def save_state(request, game):
    """ Save game state from the received postMessage """
    try:
        game_state_data = json.loads(request.POST['gameState'])
    except KeyError:
        return HttpResponseBadRequest(MESSAGE_SAVE_STATE_ERROR)

    GameState.objects.create(
        state_data=game_state_data, game=game, player=request.user
    )

    return HttpResponse()


@never_cache
def load_game(request, game):
    """ Load game for the user """
    # ToDo: currently only loads the last game
    last_state = game.get_user_last_state(request.user)

    if last_state is None:
        return HttpResponseBadRequest(MESSAGE_LOAD_GAME_ERROR)
    else:
        return JsonResponse(last_state.state_data)


@login_required
@permission_required('community.add_game', raise_exception=True)
def create_game(request):
    if request.POST:
        game = Game(developer=request.user, rating=0.0)
        form = GameForm(data=request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('community:my-inventory')
    else:
        form = GameForm()

    return render(request, 'community/game-form.html', context={'form': form, 'create': True})


@login_required
@permission_required('community.change_game', raise_exception=True)
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not request.user.develops_game(game):
        raise PermissionDenied

    if request.POST:
        form = GameForm(data=request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('community:my-inventory')
    else:
        form = GameForm(instance=game)

    return render(request, 'community/game-form.html', context={'form': form})


@login_required
@permission_required('community.add_game', raise_exception=True)
def my_inventory(request):
    games = Game.objects.games_for_developer(request.user)
    games = Game.objects.add_action(games, request.user)

    if request.is_ajax():
        return get_statistics_my_inventory(request, developer=request.user)

    return render(request, 'community/my-inventory.html', context={'games': games})


@never_cache
def get_statistics_game_info(request, game):

    data = dict()

    overall_revenue = Purchase.objects.get_stats_overall_revenue(game=game)
    games_sold = Purchase.objects.get_stats_games_sold(game=game)

    data['overall_revenue'] = overall_revenue
    data['games_sold'] = games_sold

    # Get statistics for graphs
    stats_purchases_per_month = Purchase.objects.get_stats_purchases_per_month(game=game)
    purchases_per_month_data = dict(
        months=list(stats_purchases_per_month.keys()),
        num_purchases=list(stats_purchases_per_month.values())
    )
    data["purchases_per_month"] = purchases_per_month_data

    return JsonResponse(data)



@never_cache
def get_statistics_my_inventory(request, developer):

    data = dict()

    overall_revenue = Purchase.objects.get_stats_overall_revenue(developer=developer)
    games_sold = Purchase.objects.get_stats_games_sold(developer=developer)

    data['overall_revenue'] = overall_revenue
    data['games_sold'] = games_sold

    # Get statistics for graphs
    stats_purchases_per_month = Purchase.objects.get_stats_purchases_per_month(developer=developer)
    purchases_per_month_data = dict(
        months=list(stats_purchases_per_month.keys()),
        num_purchases=list(stats_purchases_per_month.values())
    )
    data["purchases_per_month"] = purchases_per_month_data

    stats_revenue_per_game = Purchase.objects.get_stats_revenue_per_game(developer=developer)
    revenue_per_game_data = dict(
        game_names=list(stats_revenue_per_game.keys()),
        revenues=list(stats_revenue_per_game.values())
    )
    data["revenue_per_game"] = revenue_per_game_data

    return JsonResponse(data)


@login_required
@permission_required('community.play_game', raise_exception=True)
def my_games(request):
    games = Game.objects.games_for_player(request.user)
    games = Game.objects.add_action(games, request.user)
    return render(request, 'community/my-games.html', context={'games': games})


def search_by_category(request, category):
    category = get_object_or_404(GameCategory, name=category)
    games = Game.objects.filter(category=category)
    games = Game.objects.add_action(games, request.user)
    context = {
        'category': category.name,
        'games': games,
    }
    return render(request, 'community/search-category.html', context=context)


def search_by_query(request):
    try:
        query = request.GET['q']
    except KeyError:
        return defaults.bad_request(request=request, exception=KeyError)

    matches = Game.objects.filter(name__search=query)
    matches = Game.objects.add_action(matches, request.user)

    context = {
        'query': query,
        'matches': matches
    }

    return render(request, 'community/search-query.html', context=context)
