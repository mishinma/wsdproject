import json

from django.urls import reverse
from django.test import TestCase, RequestFactory

from accounts.models import UserMethods
from haze.settings import PAYMENT_SID
from community.models import Game
from webshop import views
from webshop.models import PendingTransaction
from base.tests.status_codes import BAD_REQUEST_400


class PendingTransactionModelTestCase(TestCase):

    fixtures = ['test_users', 'test_games']

    def setUp(self):
        self.sansa_player = UserMethods.objects.get(username='sansa')
        self.game3 = Game.objects.get(id=3)

    def test_create_new_pending(self):

        pending_transaction = PendingTransaction.objects.create_new_pending(
            user=self.sansa_player, game=self.game3, amount=19.99
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
            data={'amount': 15.0}
        )
        request.user = self.ned_player

        response = views.purchase_pending(request, self.game3)
        response_data = json.loads(response.content.decode('utf-8'))

        test_response_data = {
            'pid': 2,
            'sid': PAYMENT_SID,
            'amount': '15.0',
            'checksum': '8321ae6b5f68c73f7a25096a459b2ece',
            'success_url': 'http://testserver/shop/buy/callback',
            'cancel_url': 'http://testserver/shop/buy/callback',
            'error_url': 'http://testserver/shop/buy/callback',
        }

        self.assertEqual(response_data, test_response_data)

