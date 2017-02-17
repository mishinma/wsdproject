from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest

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

    else:
        # Determine price
        if game.sales_price is not None and game.sales_price < game.price:
            amount = game.sales_price
        else:
            amount = game.price

        form = PendingTransactionForm()
        context = {
            'url': 'http://payments.webcourse.niksula.hut.fi/pay/',
            'game': game,
            'form': form,
            'price': amount,
            }
        return render(request, 'webshop/purchase-form.html', context=context)


def purchase_pending(request, game):

    # Get amount from request, so that the user gets charged exactly
    # that was shown to him.
    try:
        amount = request.POST['amount']
    except KeyError:
        return HttpResponseBadRequest(MESSAGE_PURCHASE_PENDING_ERROR)

    new_pt = PendingTransaction.objects.create_new_pending(
        user=request.user, game=game, amount=amount)

    callback_url = request.build_absolute_uri(
        reverse('webshop:purchase-callback')
    )

    response_data = {
        'pid': new_pt.pid,
        'sid': PAYMENT_SID,
        'amount': amount,
        'success_url': callback_url,
        'cancel_url': callback_url,
        'error_url': callback_url,
        'checksum': new_pt.checksum
    }
    
    return JsonResponse(response_data)


@login_required
@permission_required('community.buy_game', raise_exception=True)
def purchase_callback(request):
    pass
    # Get passed parameters
    try:
        pid = request.GET['pid']
        ref = request.GET['ref']
        result = request.GET['result']
        checksum = request.GET['checksum']
    except KeyError:
        return defaults.bad_request(request=request, exception=KeyError)
    # Get referenced pending transaction
    try:
        pending_transaction = PendingTransaction.objects.get(pid=pid)
    except PendingTransaction.DoesNotExist:
        return defaults.bad_request(
            request=request,
            exception=PendingTransaction.DoesNotExist
        )

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
            transaction.user.games.add(purchase_game)
            return redirect('community:game-play', game_id=purchased_game.id)
        elif result == 'cancel':
            return redirect(
                'webshop:purchase-game',
                game_id=pending_transaction.game.id
            )
        elif result == 'error':
            return redirect(
                'webshop:purchase-game',
                game_id=pending_transaction.game.id
            )
        else:
            pass

    return defaults.bad_request(
        request=request,
        exception=SuspiciousOperation
    )
