from django.test import TestCase

from accounts.models import UserMethods
from community.models import Game
from webshop.models import PendingTransaction


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