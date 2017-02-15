from decimal import Decimal

from django.urls import reverse
from django.test import TestCase
from accounts.models import UserMethods
from community.models import Game, Game_Category
from base.tests.status_codes import FORBIDDEN_403, FOUND_302


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

        self.assertEqual(response.status_code, FOUND_302)
        self.assertEqual(response.url, reverse('base:index'))

        # Check data
        test_game = Game.objects.get(name='The Test Game 2')
        self.assertEqual(test_game.price, Decimal('11.11'))
        self.assertEqual(test_game.sales_price, Decimal('22.22'))
        self.assertEqual(test_game.source_url, 'http://test2.test')
        self.assertEqual(test_game.developer.id, self.bran_developer.id)
        self.assertEqual(test_game.rating, Decimal('0.0'))

    def test_edit_game(self):
        game = Game.objects.create(
            developer=self.bran_developer,
            category=self.rpg_cat,
            source_url='http://test3.test',
            price=11.20,
            sales_price=10.01,
            name='The Test Game 3',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                        'in felis odio. Suspendisse tristique vestibulum feugiat. '
                        'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. ',
            rating=3.1
        )
        success = self.client.login(username='bran', password='bran')
        response = self.client.post(
            path=reverse('community:game-edit', kwargs={'game_id': game.id}),
            data=dict(category=self.rpg_cat.id,
                      source_url='http://test4.test',
                      price=11.25,
                      sales_price=9.99,
                      name='The Awesome Test Game 3',
                      description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                                  'in felis odio. Suspendisse tristique vestibulum feugiat. '
                                  'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. ')
        )

        self.assertEqual(response.status_code, FOUND_302)
        self.assertEqual(response.url, reverse('base:index'))

        # Check data
        changed_game = Game.objects.get(name='The Awesome Test Game 3')
        self.assertEqual(changed_game.price, Decimal('11.25'))
        self.assertEqual(changed_game.sales_price, Decimal('9.99'))
        self.assertEqual(changed_game.source_url, 'http://test4.test')
        self.assertEqual(changed_game.developer.id, self.bran_developer.id)
        self.assertEqual(changed_game.rating, Decimal('3.1'))

    def test_edit_game_try_set_rating(self):
        game = Game.objects.create(
            developer=self.bran_developer,
            category=self.rpg_cat,
            source_url='http://test3.test',
            price=11.20,
            sales_price=10.01,
            name='The Test Game 3',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                        'in felis odio. Suspendisse tristique vestibulum feugiat. '
                        'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. ',
            rating=3.1
        )
        success = self.client.login(username='bran', password='bran')
        response = self.client.post(
            path=reverse('community:game-edit', kwargs={'game_id': game.id}),
            data=dict(category=self.rpg_cat.id,
                      source_url='http://test3.test',
                      price=11.20,
                      sales_price=10.01,
                      name='The Test Game 3',
                      description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                                  'in felis odio. Suspendisse tristique vestibulum feugiat. '
                                  'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. '),
                      rating=5.0
        )

        self.assertEqual(response.status_code, FOUND_302)
        self.assertEqual(response.url, reverse('base:index'))

        # Check data
        changed_game = Game.objects.get(name='The Test Game 3')
        self.assertEqual(changed_game.rating, Decimal('3.1'))

    def test_player_cannot_edit_game(self):
        game = Game.objects.create(
            developer=self.bran_developer,
            category=self.rpg_cat,
            source_url='http://test3.test',
            price=11.20,
            sales_price=10.01,
            name='The Test Game 3',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                        'in felis odio. Suspendisse tristique vestibulum feugiat. '
                        'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. ',
            rating=3.1
        )
        success = self.client.login(username='ned', password='ned')
        response = self.client.post(
            path=reverse('community:game-edit', kwargs={'game_id': game.id}),
            data=dict(category=self.rpg_cat.id,
                      source_url='http://test3.test',
                      price=0.01,
                      name='The Test Game 3',
                      description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                                  'in felis odio. Suspendisse tristique vestibulum feugiat. '
                                  'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. '),
        )
        self.assertEqual(response.status_code, FORBIDDEN_403)





