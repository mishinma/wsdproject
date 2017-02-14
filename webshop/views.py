from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from hashlib import md5
from webshop.models import Transaction, Purchase
from webshop.forms import PaymentForm
from community.models import Game
from haze.settings import PAYMENT_SID, PAYMENT_SECRET_KEY

import uuid


@login_required
@permission_required('community.play_game', raise_exception=True)
def purchase_game(request, game_id):
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    if user.owns_game(game_id):
        # User owns game already
        return redirect('community:game-play', game_id=game_id)
    else:
        pid = generate_new_pid()
        checksum = generate_checksum(pid, game.price)
        success_url = request.build_absolute_uri(reverse('webshop:purchase-success'))
        cancel_url = request.build_absolute_uri(reverse('webshop:purchase-cancel'))
        error_url = request.build_absolute_uri(reverse('webshop:purchase-error'))
        if(game.sales_price is not None and game.sales_price < game.price):
            price = game.sales_price
        else:
            price = game.price
        form = PaymentForm(initial={
                                    'developer': game.developer.username,
                                    'price': price
                                    }, payer_id=user.id)
        context = {
            'pid': pid,
            'sid': PAYMENT_SID,
            'amount': game.price,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'error_url': error_url,
            'checksum': checksum,
            'url': 'http://payments.webcourse.niksula.hut.fi/pay/',
            'game': game,
            'form': form
            }
        return render(request, 'webshop/purchase-form.html', context=context)


def success(request):
    pass


def cancel(request):
    pass


def error(request):
    pass


# Generate random, alpha-numeric, 32 character long string
def generate_new_pid():
    return str(uuid.uuid4()).replace('-', '')


def generate_checksum(pid, amount):
    checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid, PAYMENT_SID,
                                                             amount, PAYMENT_SECRET_KEY)
    generator = md5(checksum_str.encode('ascii'))
    return generator.hexdigest()
