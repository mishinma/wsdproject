from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Developer
from community.models import Game, Game_Category


class GameTestCase(TestCase):
    def setUp(self):
        jon_user = User.objects.create(username='jon', password='bastard')
        jon_developer = Developer.objects.create(user=jon_user)
        rpg_cat = Game_Category.objects.create(name='RPG')
        Game.objects.create(
            developer=jon_developer,
            category=rpg_cat,
            source_url='got.test',
            price=50.00,
            sales_price=49.99,
            name='The Battle of the Bastards',
            description='The Battle of the Bastards is a battle late in the War '
                        'of the Five Kings in which Jon Snow and Sansa Stark retake '
                        'Winterfell from Lord Ramsay Bolton, the Warden of the North, '
                        'and restore House Stark as the ruling house of the North. ',
            rating=4.5
        )

    def test_game_init(self):
        rpg_cat = Game_Category.objects.get(name='RPG')
        got_game = Game.objects.get(name='The Battle of the Bastards')