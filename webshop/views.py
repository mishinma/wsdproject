from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views import defaults

from webshop.models import Transaction, PendingTransaction
from webshop.forms import PendingTransactionForm
from community.models import Game
from haze.settings import PAYMENT_SID


@login_required
@permission_required('community.buy_game', raise_exception=True)
def purchase_game(request, game_id):
    user = request.user
    game = get_object_or_404(Game, id=game_id)

    if user.plays_game(game):
        # User owns game already
        return redirect('community:game-play', game_id=game_id)

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


@login_required
@permission_required('community.buy_game', raise_exception=True)
def purchase_pending(request):
    try:
        game_id, amount = extract_post_callback_data(request)
    except KeyError:
        return defaults.bad_request(request=request, exception=KeyError)

    if request.is_ajax():
        user = request.user
        game = Game.objects.get(id=game_id)

        new_pt = PendingTransaction.objects.create_new_pending(
            user=user, game=game, amount=amount)

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
    else:
        return defaults.bad_request(
            request=request,
            exception=SuspiciousOperation
        )


@login_required
@permission_required('community.buy_game', raise_exception=True)
def purchase_callback(request):
    # Get passed parameters
    try:
        pid, ref, result, checksum_received = extract_get_callback_data(request)
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


def extract_post_callback_data(request):
    game_id = request.POST['game']
    amount = request.POST['amount']

    return game_id, amount


def extract_get_callback_data(request):
    pid = request.GET['pid']
    ref = request.GET['ref']
    result = request.GET['result']
    checksum = request.GET['checksum']

    return pid, ref, result, checksum
