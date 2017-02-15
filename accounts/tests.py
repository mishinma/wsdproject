from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserMethods
from community.models import Game, Game_Category
from base.tests.status_codes import OK_200, SEE_OTHER_303

# Any resemblance to Game of Thrones characters is purely coincidental


class UserMethodsTestCase(TestCase):

    fixtures = [
        'test_users',
        'test_game_categories',
        'test_games'
    ]

    def setUp(self):
        self.ned_player = UserMethods.objects.get(username='ned')
        self.bran_developer = UserMethods.objects.get(username='bran')
        self.game1 = Game.objects.get(name='The Battle of the Bastards')
        self.game2 = Game.objects.get(name='The Test Game')

    def test_player_plays_game_true(self):
        self.assertTrue(self.ned_player.plays_game(self.game2))

    def test_player_plays_game_false(self):
        self.assertFalse(self.ned_player.plays_game(self.game1))

    def test_developer_develops_game_true(self):
        self.assertTrue(self.bran_developer.develops_game(self.game1))

    def test_developer_develops_game_false(self):
        self.assertFalse(self.bran_developer.develops_game(self.game2))


class RegisterViewTestCase(TestCase):

    fixtures = [
        'test_users',
        'test_game_categories',
        'test_games'
    ]

    def test_register_new_player(self):
        response = self.client.post(
            path=reverse('accounts:register-user'),
            data={
                'username': 'jon',
                'email': 'jon.snow@aalto.fi',
                'password': 'asdf',
                'confirm_password': 'asdf',
                'is_developer': False
            })

        # Redirect to user
        self.assertEqual(response.status_code, SEE_OTHER_303)
        self.assertEqual(response.url, reverse('base:index'))

        # Check user data and permissions
        jon_player = User.objects.get(username='jon')
        self.assertEqual(jon_player.email, 'jon.snow@aalto.fi')
        self.assertTrue(jon_player.check_password('asdf'))
        self.assertTrue(jon_player.has_perm('community.play_game'))
        self.assertFalse(jon_player.has_perm('community.create_game'))
        self.assertFalse(jon_player.has_perm('community.delete_game'))
        self.assertFalse(jon_player.has_perm('community.edit_game'))

    def test_register_new_developer(self):
        response = self.client.post(
            path=reverse('accounts:register-user'),
            data={
                'username': 'daenerys',
                'email': 'daenerys.targerian@aalto.fi',
                'password': 'fdsa',
                'confirm_password': 'fdsa',
                'is_developer': True
            })
        # Redirect to user
        self.assertEqual(response.status_code, SEE_OTHER_303)
        self.assertEqual(response.url, reverse('base:index'))

        # Check user data and permissions
        dany_developer = User.objects.get(username='daenerys')
        self.assertEqual(dany_developer.email, 'daenerys.targerian@aalto.fi')
        self.assertTrue(dany_developer.check_password('fdsa'))
        self.assertFalse(dany_developer.has_perm('community.play_game'))
        self.assertTrue(dany_developer.has_perm('community.add_game'))
        self.assertTrue(dany_developer.has_perm('community.delete_game'))
        self.assertTrue(dany_developer.has_perm('community.change_game'))

    def test_register_password_mismatch(self):
        response = self.client.post(
            path=reverse('accounts:register-user'),
            data={
                'username': 'ramsey',
                'email': 'ramsey.bolton@aalto.fi',
                'password': 'asdfasdf',
                'confirm_password': 'asdf',
                'is_developer': False
            })
        self.assertEqual(response.status_code, OK_200)
        with self.assertRaises(User.DoesNotExist):
            ramsey_player = User.objects.get(username='ramsey')

