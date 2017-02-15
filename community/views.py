from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, PermissionDenied
from community.models import Game, Game_Score, Game_State
from community.forms import GameForm
import json


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})


@login_required
@permission_required('community.play_game', raise_exception=True)
def play_game(request, game_id):

    game = get_object_or_404(Game, id=game_id)
    if request.user.plays_game(game):

        if request.POST.get("messageType") == "SCORE":
            score = Game_Score(score=request.POST.get("score"), game=game, player=request.user)
            score.save()

        # TODO: add top scores
        context = {
            'game': game,
            'user_high_score': game.get_user_highest_score(request.user),
            'user_last_score': game.get_user_latest_score(request.user),
        }
        return render(request, "community/game-play.html", context)
    else:
        return redirect('community:game-info', game_id=game_id)


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

def save_state(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    data = json.loads(request.body.decode('utf-8'))
    state = Game_State(state_data=data, game=game, player=request.user)
    state.save()
    return render(request, "community/game-play.html")

