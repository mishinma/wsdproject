from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.


class RegisterTestCase(TestCase):
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
