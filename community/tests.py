import json
from decimal import Decimal

from django.urls import reverse
from django.test import TestCase, RequestFactory, Client

from accounts.models import UserMethods
from community import views
from community.views import MESSAGE_SAVE_SCORE_ERROR, MESSAGE_LOAD_GAME_ERROR, \
    MESSAGE_SAVE_STATE_ERROR
from community.models import Game, GameCategory, GameScore, GameState
from base.tests.status_codes import FORBIDDEN_403, FOUND_302, BAD_REQUEST_400


class GameModelTestCase(TestCase):

    # Mind the order
    fixtures = ['test_users',
                'test_games',
                'test_game_scores',
                'test_game_states']

    def setUp(self):
        self.sansa_player = UserMethods.objects.get(username='sansa')
        self.ned_player = UserMethods.objects.get(username='ned')
        self.bran_developer = UserMethods.objects.get(username='bran')
        self.game2 = Game.objects.get(id=2)
        self.game3 = Game.objects.get(id=3)
        self.game4 = Game.objects.get(id=4)

    def test_game_get_user_highest_score(self):
        sansa_game_highest_score = self.game2.get_user_high_score(self.sansa_player)
        self.assertEqual(sansa_game_highest_score, 54)

    def test_game_get_user_latest_score(self):
        sansa_game_latest_score = self.game2.get_user_last_score(self.sansa_player)
        self.assertEqual(sansa_game_latest_score, 3)

    def test_game_get_user_last_state(self):
        test_sansa_game2_last_state = {
            "score": 42,
            "items": [
                "sword"
            ]
        }
        last_state = self.game2.get_user_last_state(self.sansa_player)
        self.assertEqual(last_state.state_data, test_sansa_game2_last_state)

    def test_game_get_top3_scores(self):
        test_game_top3_scores = [score.score for score in self.game2.get_top_scores(3)]
        self.assertEqual(test_game_top3_scores, [54, 25, 12])

    def test_game_manager_games_for_developer(self):
        bran_develops_games = {game.id for game in Game.objects.games_for_developer(self.bran_developer)}
        self.assertEqual(bran_develops_games, {1, 3, 4})

    def test_game_manager_games_for_player_multiple_games(self):
        sansa_playes_games = {game.id for game in Game.objects.games_for_player(self.sansa_player)}
        self.assertEqual(sansa_playes_games, {1, 2})

    def test_game_manager_games_for_player_one_game(self):
        ned_playes_games = {game.id for game in Game.objects.games_for_player(self.ned_player)}
        self.assertEqual(ned_playes_games, {2})

    def test_game_get_price_no_sale(self):
        real_price = self.game3.get_price()
        self.assertEqual(real_price, Decimal("15.00"))

    def test_game_get_price_on_sale(self):
        real_price = self.game4.get_price()
        self.assertEqual(real_price, Decimal("10.00"))  # Real price 20.00


class GameCreateEditViewTestCase(TestCase):

    # Mind the order
    fixtures = ['test_users',
                'test_games']

    def setUp(self):
        self.rpg_cat = GameCategory.objects.get(name='RPG')
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
        self.assertEqual(response.url, reverse('community:my-inventory'))

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
        self.assertEqual(response.url, reverse('community:my-inventory'))

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
        self.assertEqual(response.url, reverse('community:my-inventory'))

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


class PlayGameViewTestCase(TestCase):

    # Mind the order
    fixtures = ['test_users',
                'test_games']

    def setUp(self):
        self.rpg_cat = GameCategory.objects.get(name='RPG')
        self.bran_developer = UserMethods.objects.get(username='bran')
        self.sansa_player = UserMethods.objects.get(username='sansa')
        self.ned_player = UserMethods.objects.get(username='ned')
        self.game1 = Game.objects.get(name='The Battle of the Bastards')
        self.game2 = Game.objects.get(name='The Test Game')
        self.factory = RequestFactory()

    def test_save_score(self):
        test_score = 64
        request = self.factory.post(
            path=reverse('community:game-play', kwargs={'game_id': self.game2.id}),
            data={'score': test_score}
        )
        request.user = self.sansa_player
        views.save_score(request, self.game2)

        sansa_new_high_score = self.game2.get_user_high_score(self.sansa_player)
        sansa_new_last_score = self.game2.get_user_last_score(self.sansa_player)

        self.assertEqual(sansa_new_high_score, test_score)
        self.assertEqual(sansa_new_last_score, test_score)

    def test_save_score_bad_message(self):
        request = self.factory.post(
            path=reverse('community:game-play', kwargs={'game_id': self.game2.id}),
            data={'not_a_score': 64}
        )
        request.user = self.sansa_player
        response = views.save_score(request, self.game2)

        self.assertEqual(response.status_code, BAD_REQUEST_400)
        self.assertEqual(response.content.decode('utf-8'), MESSAGE_SAVE_SCORE_ERROR)

    def test_save_state(self):
        test_game_state = dict(
            score=64,
            playerItems=['shield', 'sword']
        )
        test_game_state_json = json.dumps(test_game_state)
        request = self.factory.post(
            path=reverse('community:game-play', kwargs={'game_id': self.game2.id}),
            data={'gameState': test_game_state_json}
        )

        request.user = self.sansa_player
        views.save_state(request, self.game2)
        last_state = self.sansa_player.gamestate_set.order_by('-timestamp').first()

        self.assertEqual(last_state.state_data, test_game_state)

    def test_save_state_bad_message(self):
        request = self.factory.post(
            path=reverse('community:game-play', kwargs={'game_id': self.game2.id}),
            data={'not-a-gameState': {'kingdoms': 7}}
        )
        request.user = self.sansa_player
        response = views.save_state(request, self.game2)

        self.assertEqual(response.status_code, BAD_REQUEST_400)
        self.assertEqual(response.content.decode('utf-8'), MESSAGE_SAVE_STATE_ERROR)

    def test_load_game(self):
        test_state_data = {"score": 104, "items": ["sword", "shotgun"]}
        GameState.objects.create(
            player=self.sansa_player,
            game=self.game2,
            state_data=test_state_data
        )

        request = self.factory.post(
            path=reverse('community:game-play', kwargs={'game_id': self.game2.id}),
            data=dict()
        )
        request.user = self.sansa_player
        response = views.load_game(request, self.game2)
        loaded_state = json.loads(response.content.decode('utf-8'))

        self.assertEqual(loaded_state, test_state_data)

    def test_load_game_does_not_exist(self):
        request = self.factory.post(
            path=reverse('community:game-play', kwargs={'game_id': self.game1.id}),
            data=dict()
        )
        request.user = self.ned_player
        response = views.load_game(request, self.game1)

        self.assertEqual(response.status_code, BAD_REQUEST_400)
        self.assertEqual(response.content.decode('utf-8'), MESSAGE_LOAD_GAME_ERROR)


class SearchByQueryViewTestCase(TestCase):

    # Mind the order
    fixtures = ['test_users',
                'test_games']

    def setUp(self):
        self.game1 = Game.objects.get(name='The Battle of the Bastards')
        self.game2 = Game.objects.get(name='The Test Game')
        self.game3 = Game.objects.get(name='The Action Game')
        self.game4 = Game.objects.get(name='The Second Action Game')
        self.factory = RequestFactory()
        self.client = Client()

    def test_query_does_not_exist(self):
        request = self.factory.get(
            path=reverse('community:search-query'), data={'asdf': 'foo'}
        )

        response = views.search_by_query(request)

        self.assertEqual(response.status_code, BAD_REQUEST_400)

    def test_search_for_exact_name(self):
        response = self.client.get(
            reverse('community:search-query'),
            {'q': self.game1.name}
        )

        matches = response.context['matches']

        self.assertEqual(matches[0].name, self.game1.name)

    def test_search_with_query(self):
        response = self.client.get(
            reverse('community:search-query'),
            {'q': 'game'}
        )
        
        matches = response.context['matches']
        matches_id_set = {match.id for match in matches}

        self.assertEqual(matches_id_set, {self.game2.id, self.game3.id, self.game4.id})