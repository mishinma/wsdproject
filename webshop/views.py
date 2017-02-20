from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.views import defaults
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.cache import never_cache

from webshop.models import Transaction, PendingTransaction
from webshop.forms import PendingTransactionForm
from community.models import Game
from haze.settings import PAYMENT_SID

MESSAGE_PURCHASE_PENDING_ERROR = "An error occurred while processing your request."


@login_required
@permission_required('community.buy_game', raise_exception=True)
def purchase_game(request, game_id):

    game = get_object_or_404(Game, id=game_id)

    if request.user.plays_game(game):
        # User owns game already
        return redirect('community:game-play', game_id=game_id)

    if request.is_ajax():
        return purchase_pending(request, game)

    form = PendingTransactionForm()
    context = {
        'url': 'http://payments.webcourse.niksula.hut.fi/pay/',
        'game': game,
        'form': form,
        }
    return render(request, 'webshop/purchase-form.html', context=context)


@never_cache
def purchase_pending(request, game):

    new_pt = PendingTransaction.objects.create_new_pending(user=request.user, game=game)

    callback_url = request.build_absolute_uri(
        reverse('webshop:purchase-callback')
    )

    response_data = {
        'pid': new_pt.pid,
        'sid': PAYMENT_SID,
        'amount': new_pt.amount,
        'success_url': callback_url,
        'cancel_url': callback_url,
        'error_url': callback_url,
        'checksum': new_pt.checksum
    }

    return JsonResponse(response_data)


@login_required
@permission_required('community.buy_game', raise_exception=True)
def purchase_callback(request):

    # Get passed parameters
    try:
        pid = request.GET['pid']
        ref = request.GET['ref']
        result = request.GET['result']
        checksum_received = request.GET['checksum']
    except KeyError:
        return defaults.bad_request(request=request, exception=KeyError)

    pending_transaction = get_object_or_404(PendingTransaction, pk=pid)

    checksum_valid = pending_transaction.validate_checksum(
        checksum=checksum_received, ref=ref, result=result)

    # Handle callback according to result
    if checksum_valid:
        transaction, purchase = Transaction.objects.create_from_pending(
            pending_transaction=pending_transaction,
            ref=ref,
            result=result
        )
        if result == 'success':
            purchased_game = pending_transaction.game
            transaction.user.games.add(purchased_game)
            return redirect('community:game-play', game_id=purchased_game.id)
        elif result == 'cancel' or result == 'error':
            return redirect(
                'webshop:purchase-game',
                game_id=pending_transaction.game.id
            )
    else:

        return defaults.bad_request(
            request=request,
            exception=SuspiciousOperation
        )
