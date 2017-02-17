from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views import defaults

from webshop.models import Transaction, PendingTransaction
from webshop.forms import PendingTransactionForm
from community.models import Game
from haze.settings import PAYMENT_SID, PAYMENT_SECRET_KEY


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
        pid = Transaction.generate_new_pid(game=game, user=user)
        checksum = Transaction.generate_checksum(
            pid=pid,
            sid=PAYMENT_SID,
            amount=amount,
            token=PAYMENT_SECRET_KEY
        )

        callback_url = request.build_absolute_uri(
            reverse('webshop:purchase-callback')
        )

        PendingTransaction.objects.create(
            user=user,
            pid=pid,
            game=game,
            amount=amount
        )
        response_data = {
            'pid': pid,
            'sid': PAYMENT_SID,
            'amount': amount,
            'success_url': callback_url,
            'cancel_url': callback_url,
            'error_url': callback_url,
            'checksum': checksum
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
    # Compute checksum
    valid_checksum = Transaction.validate_received_checksum(
        checksum=checksum_received,
        pid=pid,
        ref=ref,
        result=result,
        token=PAYMENT_SECRET_KEY
    )
    # Handle callback according to result
    if valid_checksum:
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
