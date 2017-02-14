from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from community.models import Game, Game_Score, Game_State
from community.forms import GameForm


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})


@login_required
@permission_required('community.play_game', raise_exception=True)
def play_game(request, game_id):

    game = get_object_or_404(Game, id=game_id)
    if request.user.plays_game(game):

        if request.method == "POST" and request.POST.get("messageType") == "SCORE":
            score = Game_Score(score=request.POST.get("score"), game=game, player=request.user)
            score.save()

        if request.method == "POST" and request.POST.get("messageType") == "SAVE":
            state = Game_State(state_data=request.POST.get("gameState"), game=game, player=request.user)
            state.save()

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
            return redirect('base:index')
    else:
        form = GameForm()
    return render(request, 'community/game-form.html', context={'form': form})


def edit_game(request):
    pass
