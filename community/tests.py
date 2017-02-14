import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User, Group
from community.models import Game, Game_Category, Game_Score


class GameTestCase(TestCase):
    def setUp(self):
        # Create a developer
        developer_group = Group.objects.get(name='developer')
        jon = User.objects.create(username='jon', password='bastard')
        jon.groups.add(developer_group)

        # Create a category
        rpg_cat = Game_Category.objects.create(name='RPG')

        # Create a game
        game = Game.objects.create(
            developer=jon,
            category=rpg_cat,
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

        # Create players
        player_group = Group.objects.get(name='player')
        sansa = User.objects.create(username='sansa', password='sansa')
        sansa.groups.add(player_group)
        bran = User.objects.create(username='bran', password='bran')
        bran.groups.add(player_group)

        # Create scores
        gs1 = Game_Score.objects.create(player=sansa, game=game, score=3,
                                        timestamp=datetime.datetime(2017, 2, 14, 9, 12, 41, 226088,
                                                                    tzinfo=timezone.utc))
        gs2 = Game_Score.objects.create(player=bran, game=game, score=12,
                                        timestamp=datetime.datetime(2017, 2, 14, 10, 43, 11, 226088,
                                                                    tzinfo=timezone.utc))
        gs3 = Game_Score.objects.create(player=sansa, game=game, score=54,
                                        timestamp=datetime.datetime(2017, 2, 15, 9, 12, 41, 226088,
                                                                    tzinfo=timezone.utc))
        gs4 = Game_Score.objects.create(player=bran, game=game, score=25,
                                        timestamp=datetime.datetime(2017, 2, 16, 1, 30, 21, 226088,
                                                                    tzinfo=timezone.utc))

    def test_game_init(self):
        rpg_cat = Game_Category.objects.get(name='RPG')
        got_game = Game.objects.get(name='The Battle of the Bastards')

    def test_game_get_user_highest_score(self):
        sansa = User.objects.get(username='sansa')
        game = Game.objects.get(name='The Battle of the Bastards')
        sansa_game_highest_score = game.get_user_highest_score(sansa)
        self.assertEqual(sansa_game_highest_score, 54)

    def test_game_get_user_latest_score(self):
        sansa = User.objects.get(username='sansa')
        game = Game.objects.get(name='The Battle of the Bastards')
        sansa_game_latest_score = game.get_user_latest_score(sansa)
        self.assertEqual(sansa_game_latest_score,
                         datetime.datetime(2017, 2, 15, 9, 12, 41, 226088, tzinfo=timezone.utc))
