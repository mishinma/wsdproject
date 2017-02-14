from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from webshop.models import Transaction
from webshop.forms import PendingTransactionForm
from community.models import Game
from haze.settings import PAYMENT_SID, PAYMENT_SECRET_KEY


@login_required
@permission_required('community.play_game', raise_exception=True)
def purchase_game(request, game_id):
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    if user.owns_game(game_id):
        # User owns game already
        return redirect('community:game-play', game_id=game_id)
    else:
        # Determine price
        if(game.sales_price is not None and game.sales_price < game.price):
            amount = game.sales_price
        else:
            amount = game.price
        pid = Transaction.generate_new_pid(game=game, user=user)
        checksum = Transaction.generate_checksum(pid=pid, sid=PAYMENT_SID,
                                                 amount=amount,
                                                 token=PAYMENT_SECRET_KEY)
        success_url = request.build_absolute_uri(reverse('webshop:purchase-success'))
        cancel_url = request.build_absolute_uri(reverse('webshop:purchase-cancel'))
        error_url = request.build_absolute_uri(reverse('webshop:purchase-error'))

        form = PendingTransactionForm(initial={
            'user': user.id,
            'pid': pid,
            'sid': PAYMENT_SID,
            'amount': amount,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'error_url': error_url,
            'checksum': checksum
        })
        context = {
            'url': 'http://payments.webcourse.niksula.hut.fi/pay/',
            'game': game,
            'form': form,
            'price': amount,
            }
        return render(request, 'webshop/purchase-form.html', context=context)


def success(request):
    pass


def cancel(request):
    pass


def error(request):
    pass
