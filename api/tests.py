from django.test import TestCase, Client
from accounts.models import UserMethods
from community.models import Game, GameCategory, GameScore
from django.urls import reverse
from base.tests.status_codes import NOT_FOUND_404, BAD_REQUEST_400, OK_200


# Create your tests here.
class GetGamesOfCategoryViewTestCase(TestCase):
    fixtures = ['test_users',
                'test_games']

    def setUp(self):
        self.cat1 = GameCategory.objects.get(id=1)
        self.client = Client()
        self.callback = 'foo'

    def test_category_does_not_exist(self):
        response = self.client.get(
            path=reverse('api:cat-games', kwargs={'category': 'asdfasdf'})
            )

        self.assertEqual(response.status_code, NOT_FOUND_404)
        self.assertEqual(response.json()['error'], NOT_FOUND_404)

    def test_category_exists(self):
        response = self.client.get(
            path=reverse('api:cat-games', kwargs={'category': self.cat1.name})
            )
        num_games = Game.objects.filter(category=self.cat1).count()
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(response.json()), num_games)

    def test_category_name_case_insensitive(self):
        response = self.client.get(
            path=reverse('api:cat-games', kwargs={'category': self.cat1.name.lower()})
            )
        num_games = Game.objects.filter(category=self.cat1).count()
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(response.json()), num_games)

    def test_jsonp(self):
        response = self.client.get(
            reverse('api:cat-games', kwargs={'category': self.cat1.name}),
            {'callback': self.callback}
            )
        self.assertTrue(str(response.content, 'utf-8').startswith(self.callback + '('))
        self.assertTrue(str(response.content, 'utf-8').endswith(')'))


class GetGamesOfDevViewTestCase(TestCase):
    fixtures = ['test_users',
                'test_games']

    def setUp(self):
        self.dev = UserMethods.objects.get(id=1)
        self.non_dev = UserMethods.objects.get(id=3)
        self.client = Client()
        self.callback = 'foo'

    def test_dev_does_not_exist(self):
        response = self.client.get(
            path=reverse('api:dev-games', kwargs={'dev_id': 0})
            )

        self.assertEqual(response.status_code, NOT_FOUND_404)
        self.assertEqual(response.json()['error'], NOT_FOUND_404)

    def test_dev_does_exist(self):
        response = self.client.get(
            path=reverse('api:dev-games', kwargs={'dev_id': self.dev.id})
            )
        num_games = Game.objects.filter(developer=self.dev).count()
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(response.json()), num_games)

    def test_specified_user_is_no_dev(self):
        response = self.client.get(
            path=reverse('api:dev-games', kwargs={'dev_id': self.non_dev.id})
            )
        self.assertTrue(not self.non_dev.is_developer())
        self.assertEqual(response.status_code, BAD_REQUEST_400)
        self.assertEqual(response.json()['error'], BAD_REQUEST_400)

    def test_jsonp(self):
        response = self.client.get(
            reverse('api:dev-games', kwargs={'dev_id': self.dev.id}),
            {'callback': self.callback}
            )
        self.assertTrue(str(response.content, 'utf-8').startswith(self.callback + '('))
        self.assertTrue(str(response.content, 'utf-8').endswith(')'))


class GetGameDetailViewTestCase(TestCase):
    fixtures = ['test_users',
                'test_games']

    def setUp(self):
        self.game1 = Game.objects.get(id=1)
        self.dev = UserMethods.objects.get(id=1)
        self.client = Client()
        self.callback = 'foo'

    def test_game_does_not_exist(self):
        response = self.client.get(
            path=reverse('api:game-detail', kwargs={'game_id': 0})
            )
        self.assertEqual(response.status_code, NOT_FOUND_404)
        self.assertEqual(response.json()['error'], NOT_FOUND_404)

    def test_game_does_exist(self):
        response = self.client.get(
            path=reverse('api:game-detail', kwargs={'game_id': self.game1.id})
            )
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(response.json()['name'], self.game1.name)
        self.assertEqual(response.json()['description'], self.game1.description)
        self.assertEqual(response.json()['developer_id'], self.game1.developer.id)
        self.assertEqual(response.json()['developer_name'], self.game1.developer.username)
        self.assertEqual(response.json()['category_id'], self.game1.category.id)
        self.assertEqual(response.json()['category_name'], self.game1.category.name)
        self.assertEqual(response.json()['price'], str(self.game1.price))
        self.assertEqual(response.json()['sales_price'], str(self.game1.sales_price))

    def test_jsonp(self):
        response = self.client.get(
            reverse('api:game-detail', kwargs={'game_id': self.game1.id}),
            {'callback': self.callback}
            )
        self.assertTrue(str(response.content, 'utf-8').startswith(self.callback + '('))
        self.assertTrue(str(response.content, 'utf-8').endswith(')'))


class GetScoresOfGameViewTestCase(TestCase):
    fixtures = ['test_users',
                'test_games',
                'test_game_scores']

    def setUp(self):
        self.game1 = Game.objects.get(id=1)
        self.game2 = Game.objects.get(id=2)
        self.client = Client()
        self.callback = 'foo'

    def test_game_does_not_exist(self):
        response = self.client.get(
            path=reverse('api:game-scores', kwargs={'game_id': 0})
            )
        self.assertEqual(response.status_code, NOT_FOUND_404)
        self.assertEqual(response.json()['error'], NOT_FOUND_404)

    def test_game_does_exist_with_scores(self):
        response = self.client.get(
            path=reverse('api:game-scores', kwargs={'game_id': self.game2.id})
            )
        num_scores = GameScore.objects.filter(game=self.game2).count()
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(response.json()), num_scores)

    def test_game_does_exist_without_scores(self):
        response = self.client.get(
            path=reverse('api:game-scores', kwargs={'game_id': self.game1.id})
            )
        num_scores = GameScore.objects.filter(game=self.game1).count()
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(response.json()), num_scores)

    def test_jsonp(self):
        response = self.client.get(
            reverse('api:game-scores', kwargs={'game_id': self.game2.id}),
            {'callback': self.callback}
            )
        self.assertTrue(str(response.content, 'utf-8').startswith(self.callback + '('))
        self.assertTrue(str(response.content, 'utf-8').endswith(')'))


class GetCategoriesViewTestCase(TestCase):
    fixtures = ['test_users',
                'test_games']

    def setUp(self):
        self.client = Client()
        self.callback = 'foo'

    def test_get_all_categories(self):
        response = self.client.get(
            path=reverse('api:all-cats')
            )
        num_cats = GameCategory.objects.all().count()
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(response.json()), num_cats)

    def test_jsonp(self):
        response = self.client.get(
            reverse('api:all-cats'), {'callback': self.callback}
            )
        self.assertTrue(str(response.content, 'utf-8').startswith(self.callback + '('))
        self.assertTrue(str(response.content, 'utf-8').endswith(')'))


class GetDevsViewTestCase(TestCase):
    fixtures = ['test_users']

    def setUp(self):
        self.client = Client()
        self.callback = 'foo'

    def test_get_all_devs(self):
        response = self.client.get(
            path=reverse('api:all-devs')
            )
        num_devs = UserMethods.objects.filter(groups__name='developer').count()
        self.assertEqual(response.status_code, OK_200)
        self.assertEqual(len(response.json()), num_devs)

    def test_jsonp(self):
        response = self.client.get(
            reverse('api:all-devs'), {'callback': self.callback}
            )
        self.assertTrue(str(response.content, 'utf-8').startswith(self.callback + '('))
        self.assertTrue(str(response.content, 'utf-8').endswith(')'))
