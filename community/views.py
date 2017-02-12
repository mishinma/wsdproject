from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from community.models import Game, Game_Score, Game_State
from django.db.models import Max


def game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "community/game-info.html", {'game': game})


@login_required
@permission_required('community.play_game', raise_exception=True)
def play_gamelay(request, game_id):
    if request.user.owns_game(game_id):
        game = get_object_or_404(Game, id=game_id)

        try:
            scores = Game_Score.objects.get(game=game)
            user_high_score = scores.filter(player=request.user).aggregate(Max('score'))
            user_last_score = scores.filter(player=request.user).aggregate(Max('timestamp'))
            top_players_scores = scores.order_by('score')
        except Game_Score.DoesNotExist:
            user_high_score = 0
            user_last_score = 0
            top_players_scores = 0

        try:
            state = Game_State.objects.get(game=game)
        except Game_State.DoesNotExist:
            state = {}

        context = {
            'game': game,
            'user_high_score': user_high_score,
            'user_last_score': user_last_score,
            'top_player_scores': top_players_scores,
            'state': state
        }
        return render(request, "community/game-play.html", context)
    else:
        return redirect('community:game-info', game_id=game_id)
