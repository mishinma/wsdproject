from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from community.models import Game
from community.forms import GameForm


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})


@login_required
@permission_required('community.play_game', raise_exception=True)
def play_game(request, game_id):
    if request.user.owns_game(game_id):
        game = get_object_or_404(Game, id=game_id)
        return render(request, "community/game-info.html", {'game': game})


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
