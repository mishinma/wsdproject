from decimal import Decimal

from django.urls import reverse
from django.test import TestCase
from accounts.models import UserMethods
from community.models import Game, Game_Category


class GameModelTestCase(TestCase):

    # Mind the order
    fixtures = ['test_users',
                'test_game_categories',
                'test_games',
                'test_game_scores']

    def setUp(self):
        self.sansa_player = UserMethods.objects.get(username='sansa')
        self.game2 = Game.objects.get(name='The Test Game')

    def test_game_get_user_highest_score(self):
        sansa_game_highest_score = self.game2.get_user_highest_score(self.sansa_player)
        self.assertEqual(sansa_game_highest_score, 54)

    def test_game_get_user_latest_score(self):
        sansa_game_latest_score = self.game2.get_user_latest_score(self.sansa_player)
        self.assertEqual(sansa_game_latest_score, 3)


class GameCreateEditViewTestCase(TestCase):

    # Mind the order
    fixtures = ['test_users',
                'test_game_categories',
                'test_games']

    def setUp(self):
        self.rpg_cat = Game_Category.objects.get(name='RPG')
        self.bran_developer = UserMethods.objects.get(username='bran')

    def test_create_new_game(self):
        success = self.client.login(username='bran', password='bran')
        response = self.client.post(
            path=reverse('community:game-create'),
            data=dict(category=self.rpg_cat.id,
                      source_url='http://test2.test',
                      price=11.11,
                      sales_price=22.22,
                      name='The Test Game 2',
                      description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                                  'in felis odio. Suspendisse tristique vestibulum feugiat. '
                                  'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. ')
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('base:index'))

        # Check data
        test_game = Game.objects.get(name='The Test Game 2')
        self.assertEqual(test_game.price, Decimal('11.11'))
        self.assertEqual(test_game.sales_price, Decimal('22.22'))
        self.assertEqual(test_game.source_url, 'http://test2.test')
        self.assertEqual(test_game.developer.id, self.bran_developer.id)
        self.assertEqual(test_game.rating, Decimal('0.0'))

