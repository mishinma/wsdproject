import json
from decimal import Decimal

from django.urls import reverse
from django.test import TestCase, RequestFactory

from accounts.models import UserMethods
from haze.settings import PAYMENT_SID
from community.models import Game
from webshop import views
from webshop.views import MESSAGE_PURCHASE_PENDING_ERROR
from webshop.models import PendingTransaction
from base.tests.status_codes import BAD_REQUEST_400


class PendingTransactionModelTestCase(TestCase):

    fixtures = ['test_users', 'test_games']

    def setUp(self):
        self.sansa_player = UserMethods.objects.get(username='sansa')
        self.game3 = Game.objects.get(id=3)

    def test_create_new_pending(self):

        pending_transaction = PendingTransaction.objects.create_new_pending(
            user=self.sansa_player, game=self.game3, amount=Decimal('19.99')
        )

        self.assertEqual(pending_transaction.pid, 1)
        self.assertEqual(pending_transaction.checksum, 'c4e97debfbabed651dea3c540577420c')


class PurchaseViewsTestCase(TestCase):

    fixtures = ['test_users', 'test_games', 'test_transactions']

    def setUp(self):
        self.factory = RequestFactory()
        self.ned_player = UserMethods.objects.get(username='ned')
        self.game3 = Game.objects.get(id=3)

    def test_view_purchase_pending(self):

        request = self.factory.post(
            path=reverse('webshop:purchase-game', kwargs={'game_id': self.game3.id}),
            data={'amount': '15.00'}
        )
        request.user = self.ned_player

        response = views.purchase_pending(request, self.game3)
        response_data = json.loads(response.content.decode('utf-8'))

        test_response_data = {
            'pid': 2,
            'sid': PAYMENT_SID,
            'amount': '15.00',
            'checksum': 'ceeb9afd59957bbfb50bfe270909dcda',
            'success_url': 'http://testserver/shop/buy/callback',
            'cancel_url': 'http://testserver/shop/buy/callback',
            'error_url': 'http://testserver/shop/buy/callback',
        }

        self.assertEqual(response_data, test_response_data)

    def test_view_puchase_pending_amount_not_sent(self):
        request = self.factory.post(
            path=reverse('webshop:purchase-game', kwargs={'game_id': self.game3.id}),
            data={'not-an-amount': '15.00'}
        )
        request.user = self.ned_player
        response = views.purchase_pending(request, self.game3)

        self.assertEqual(response.status_code, BAD_REQUEST_400)
        self.assertEqual(response.content.decode('utf-8'), MESSAGE_PURCHASE_PENDING_ERROR)