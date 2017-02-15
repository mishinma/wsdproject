from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, PermissionDenied
from community.models import Game, Game_Score
from django.contrib.auth.models import User
from community.forms import GameForm


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})


@login_required
@permission_required('community.play_game', raise_exception=True)
def play_game(request, game_id):

    game = get_object_or_404(Game, id=game_id)
    if request.user.plays_game(game):

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
            return redirect('base:index')
    else:
        form = GameForm(instance=game)
        
    return render(request, 'community/game-form.html', context={'form': form})