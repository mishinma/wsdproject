import json
from datetime import datetime
from decimal import Decimal

from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.utils import timezone

from accounts.models import UserMethods
from haze.settings import PAYMENT_SID
from community.models import Game, GameCategory
from webshop import views
from webshop.views import MESSAGE_PURCHASE_PENDING_ERROR
from webshop.models import PendingTransaction, Purchase
from base.tests.status_codes import BAD_REQUEST_400

from django.db import connection


class PendingTransactionModelTestCase(TestCase):

    fixtures = ['test_users', 'test_games']

    def setUp(self):
        self.sansa_player = UserMethods.objects.get(username='sansa')
        self.game3 = Game.objects.get(id=3)

    def test_create_new_pending(self):

        pending_transaction = PendingTransaction.objects.create_new_pending(
            user=self.sansa_player, game=self.game3
        )

        self.assertEqual(pending_transaction.pid, 1)
        self.assertEqual(pending_transaction.checksum, '86ed38f96b26bdb65ed9307109c37cf2')


class PurchaseManagerTestCase(TestCase):
    fixtures = ['test_users', 'test_games', 'test_transactions']

    def setUp(self):
        self.bran_developer = UserMethods.objects.get(username='bran')
        self.sansa_player = UserMethods.objects.get(username='sansa')
        self.rpg_cat = GameCategory.objects.get(name='RPG')
        self.game1 = Game.objects.get(id=1)
        self.game2 = Game.objects.get(id=2)
        self.game3 = Game.objects.get(id=3)
        self.game4 = Game.objects.get(id=4)

    def test_get_stats_purchases_per_month_filter_developer(self):
        dt = datetime(2016, 8, 30, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=dt):
            stats = Purchase.objects.get_stats_purchases_per_month(developer=self.bran_developer)
            self.assertEqual(len(stats.keys()), 7)
            self.assertEqual(stats['February'], 0)
            self.assertEqual(stats['March'], 0)
            self.assertEqual(stats['April'], 0)
            self.assertEqual(stats['May'], 1)
            self.assertEqual(stats['June'], 0)
            self.assertEqual(stats['July'], 2)
            self.assertEqual(stats['August'], 0)

    def test_get_stats_purchases_per_month_filter_game(self):
        dt = datetime(2016, 8, 30, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=dt):
            stats = Purchase.objects.get_stats_purchases_per_month(game=self.game2)
            self.assertEqual(len(stats.keys()), 7)
            self.assertEqual(stats['February'], 0)
            self.assertEqual(stats['March'], 0)
            self.assertEqual(stats['April'], 0)
            self.assertEqual(stats['May'], 1)
            self.assertEqual(stats['June'], 0)
            self.assertEqual(stats['July'], 0)
            self.assertEqual(stats['August'], 0)

    def test_get_stats_revenue_per_game(self):
        stats = Purchase.objects.get_stats_revenue_per_game(developer=self.bran_developer)
        self.assertEqual(stats[self.game1.name], Decimal("50.00"))
        self.assertEqual(stats[self.game3.name], Decimal("30.00"))
        self.assertEqual(stats[self.game4.name], Decimal("10.00"))

    def test_get_stats_overall_revenue_filter_developer(self):
        overall_revenue = Purchase.objects.get_stats_overall_revenue(developer=self.bran_developer)
        self.assertEqual(overall_revenue, Decimal("90.00"))

    def test_get_stats_overall_revenue_filter_game(self):
        overall_revenue = Purchase.objects.get_stats_overall_revenue(game=self.game3)
        self.assertEqual(overall_revenue, Decimal("30.00"))

    def test_get_stats_overall_revenue_coalese_null_to_0(self):
        new_game = Game.objects.create(
            developer=self.bran_developer,
            category=self.rpg_cat,
            source_url='http://test3.test',
            price=11.20,
            name='New Game',
            description='Lorem ipsum dolor sit amet',
            rating=3.1
        )
        overall_revenue = Purchase.objects.get_stats_overall_revenue(game=new_game)
        self.assertEqual(overall_revenue, 0)

    def test_get_stats_games_sold_filter_developer(self):
        games_sold = Purchase.objects.get_stats_games_sold(developer=self.bran_developer)
        self.assertEqual(games_sold, 4)

    def test_get_stats_games_sold_filter_game(self):
        games_sold = Purchase.objects.get_stats_games_sold(game=self.game3)
        self.assertEqual(games_sold, 2)




def restart_pending_transaction_pk(func):
    """ Decorator to restart pid sequence """
    def wrap(*args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE webshop_pendingtransaction_pid_seq RESTART WITH 2")
        return func(*args, **kwargs)

    return wrap


class PurchaseViewsTestCase(TestCase):

    fixtures = ['test_users', 'test_games', 'test_transactions']

    def setUp(self):
        self.factory = RequestFactory()
        self.ned_player = UserMethods.objects.get(username='ned')
        self.game3 = Game.objects.get(id=3)
        self.game4 = Game.objects.get(id=4)

    @restart_pending_transaction_pk
    def test_view_purchase_pending(self):

        # No sales
        request = self.factory.get(
            path=reverse('webshop:purchase-game', kwargs={'game_id': self.game3.id})
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

    @restart_pending_transaction_pk
    def test_view_purchase_pending_on_sale(self):
        # On sale

        request = self.factory.get(
            path=reverse('webshop:purchase-game', kwargs={'game_id': self.game4.id})
        )
        request.user = self.ned_player
        response = views.purchase_pending(request, self.game4)
        response_data = json.loads(response.content.decode('utf-8'))

        test_response_data = {
            'pid': 2,
            'sid': PAYMENT_SID,
            'amount': '10.00',
            'checksum': 'd74ca644794593636dda11ba5c8e5a31',
            'success_url': 'http://testserver/shop/buy/callback',
            'cancel_url': 'http://testserver/shop/buy/callback',
            'error_url': 'http://testserver/shop/buy/callback',
        }

        self.assertEqual(response_data, test_response_data)


