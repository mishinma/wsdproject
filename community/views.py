import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, PermissionDenied
from community.models import Game, GameScore, GameState
from django.contrib.auth.models import User
from community.forms import GameForm


MESSAGE_TYPE_SCORE = 'SCORE'
MESSAGE_TYPE_SAVE = 'SAVE'
MESSAGE_TYPE_LOAD_REQUEST = 'LOAD_REQUEST'
MESSAGE_TYPE_LOAD = 'LOAD'
MESSAGE_TYPE_ERROR = 'ERROR'
MESSAGE_TYPE_SETTING = 'SETTING'

BAD_MESSAGE_RESPONSE = 'Bad message'
SAVED_RESPONSE = 'Saved'


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})


@login_required
@permission_required('community.play_game', raise_exception=True)
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Redirect if the user hasn't purchased the game
    if not request.user.plays_game(game):
        return redirect('community:game-info', game_id=game_id)

    if request.is_ajax():
        message_type = request.POST.get("messageType")

        if message_type == MESSAGE_TYPE_SCORE:
            response = save_score(request, game)
            return response

        elif message_type == MESSAGE_TYPE_SAVE:
            response = save_state(request, game)
            return response

    # TODO: add top scores
    context = {
        'game': game,
        'user_high_score': game.get_user_high_score(request.user),
        'user_last_score': game.get_user_last_score(request.user),
    }

    return render(request, "community/game-play.html", context)


def save_score(request, game):

    try:
        score_value = request.POST["score"]
    except KeyError:
        return HttpResponseBadRequest(BAD_MESSAGE_RESPONSE)

    GameScore.objects.create(
        score=score_value, game=game, player=request.user)

    # Fetch the scores and update them
    user_high_score = game.get_user_high_score(request.user)
    user_last_score = game.get_user_last_score(request.user)

    return JsonResponse({
        'userHighScore': user_high_score,
        'userLastScore': user_last_score
    })


def save_state(request, game):

    try:
        game_state_data = json.loads(request.POST['gameState'])
    except KeyError:
        return HttpResponseBadRequest(BAD_MESSAGE_RESPONSE)

    GameState.objects.create(
        state_data=game_state_data, game=game, player=request.user
    )

    return HttpResponse(SAVED_RESPONSE)

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
    return render(request, 'community/my-inventory.html', context={'games': games})


@login_required
@permission_required('community.play_game', raise_exception=True)
def my_games(request):
    games = Game.objects.games_for_player(request.user)
    return render(request, 'community/my-games.html', context={'games': games})
