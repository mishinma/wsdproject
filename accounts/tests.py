from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from accounts.models import UserMethods
from community.models import Game, Game_Category

# Any resemblance to Game of Thrones characters is purely coincidental


class RegisterTestCase(TestCase):

    def setUp(self):

        # Create developers
        self.developer_group = Group.objects.get(name='developer')
        self.bran_developer = UserMethods.objects.create(username='bran', password='bran')
        self.bran_developer.groups.add(self.developer_group)
        self.tyrion_developer = UserMethods.objects.create(username='tyrion', password='tyrion')
        self.tyrion_developer.groups.add(self.developer_group)

        # Create a category
        self.rpg_cat = Game_Category.objects.create(name='RPG')

        # Create games
        self.game1 = Game.objects.create(
            developer=self.bran_developer,
            category=self.rpg_cat,
            source_url='http://got.test',
            price=50.00,
            sales_price=49.99,
            name='The Battle of the Bastards',
            description='The Battle of the Bastards is a battle late in the War '
                        'of the Five Kings in which Jon Snow and Sansa Stark retake '
                        'Winterfell from Lord Ramsay Bolton, the Warden of the North, '
                        'and restore House Stark as the ruling house of the North. ',
            rating=4.5
        )

        self.game2 = Game.objects.create(
            developer=self.tyrion_developer,
            category=self.rpg_cat,
            source_url='http://test.test',
            price=50.00,
            sales_price=49.99,
            name='The Test Game',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc '
                        'in felis odio. Suspendisse tristique vestibulum feugiat. '
                        'Sed hendrerit lacus nulla, a tristique nibh rhoncus sed. ',
            rating=3.5
        )

        # Create players
        self.player_group = Group.objects.get(name='player')
        self.sansa_player = UserMethods.objects.create(username='sansa', password='sansa')
        self.sansa_player.groups.add(self.player_group)
        self.ned_player = UserMethods.objects.create(username='ned', password='ned')
        self.ned_player.groups.add(self.player_group)

        self.sansa_player.games.add(self.game1)
        self.ned_player.games.add(self.game2)

    # Test Models
    def test_player_plays_game_true(self):
        self.assertTrue(self.sansa_player.plays_game(self.game1))

    def test_player_plays_game_false(self):
        self.assertFalse(self.sansa_player.plays_game(self.game2))

    def test_developer_develops_game_true(self):
        self.assertTrue(self.bran_developer.develops_game(self.game1))

    def test_developer_develops_game_false(self):
        self.assertFalse(self.bran_developer.develops_game(self.game2))

    # Test views
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
        self.assertEqual(response.status_code, 302)
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
        self.assertEqual(response.status_code, 302)
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
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(User.DoesNotExist):
            ramsey_player = User.objects.get(username='ramsey')

