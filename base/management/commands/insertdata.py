from django.core.management.base import BaseCommand

from community.models import Game, GameCategory
from accounts.models import EmailConfirmed
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Insert dummy data to data base'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy data'))

    # Helper function to deal with existing usernames
    def get_or_create_user(self, username, email, password, dev=False):
        if dev:
            user_group = Group.objects.get(name='developer')
        else:
            user_group = Group.objects.get(name='player')
        try:
            user = User.objects.create(username=username, email=email)
        except IntegrityError:
            # Update existing user
            user = User.objects.get(username=username)
            user.email = email
            user.groups.clear()
        else:
            user.save()
        user.set_password(password)
        user.groups.add(user_group)
        user.save()
        EmailConfirmed.objects.update_or_create(user=user, email_confirmed=True)
        return user

    # Helper function to deal with existing game names
    def get_or_create_game(self, dev, cat, url, price, name, desc, rating, sale=None):
        try:
            game = Game.objects.create(
                developer=dev,
                category=cat,
                source_url=url,
                price=price,
                sales_price=sale,
                name=name,
                description=desc,
                rating=rating
            )
        except IntegrityError:
            # Update existing game
            game = Game.objects.get(name=name)
            game.developer = dev
            game.category = cat
            game.source_url = url
            game.price = price
            game.sales_price = sale
            game.name = name
            game.description = desc
            game.rating = rating
        game.save()
        return game

    # Helper function to deal with existing category names
    def get_or_create_game_cat(self, name):
        try:
            new_cat = GameCategory.objects.create(name=name)
        except IntegrityError:
            return GameCategory.objects.get(name=name)
        else:
            new_cat.save()
            return new_cat

    def run(self):
        default_url = 'http://webcourse.cs.hut.fi/example_game.html'
        default_desc = ('The Battle of the Bastards is a battle late in the '
                        'War of the Five Kings in which Jon Snow and Sansa '
                        'Stark retake Winterfell from Lord Ramsay Bolton, the '
                        'Warden of the North, and restore House Stark as the '
                        'ruling house of the North.')
        # Game categories
        rpg_cat = self.get_or_create_game_cat('RPG')
        action_cat = self.get_or_create_game_cat('Action')
        strategy_cat = self.get_or_create_game_cat('Strategy')
        fps_cat = self.get_or_create_game_cat('FPS')
        # Users
        jon = self.get_or_create_user('jon', 'jon@snow.west', 'jon', True)
        sansa = self.get_or_create_user('sansa', 'sansa@stark.west', 'sansa', True)
        arya = self.get_or_create_user('arya', 'arya@stark.west', 'arya', True)
        bran = self.get_or_create_user('bran', 'bran@stark.west', 'bran')
        robb = self.get_or_create_user('robb', 'robb@stark.west', 'robb')
        ned = self.get_or_create_user('ned', 'ned@stark.west', 'ned')
        # Games
        game1 = self.get_or_create_game(jon, rpg_cat, default_url, 10.0,
                                        'The Battle of the Bastards 1',
                                        default_desc, 4.5)
        game2 = self.get_or_create_game(jon, rpg_cat, default_url, 20.0,
                                        'The Battle of the Bastards 2',
                                        default_desc, 4.5)
        game3 = self.get_or_create_game(jon, action_cat, default_url, 30.0,
                                        'The Battle of the Bastards 3',
                                        default_desc, 4.5)
        game4 = self.get_or_create_game(sansa, action_cat, default_url, 40.0,
                                        'The Battle of the Bastards 4',
                                        default_desc, 4.5)
        game5 = self.get_or_create_game(sansa, action_cat, default_url, 50.0,
                                        'The Battle of the Bastards 5',
                                        default_desc, 4.5)
        game6 = self.get_or_create_game(sansa, strategy_cat, default_url, 60.0,
                                        'The Battle of the Bastards 6',
                                        default_desc, 4.5)
        game7 = self.get_or_create_game(arya, strategy_cat, default_url, 70.0,
                                        'The Battle of the Bastards 7',
                                        default_desc, 4.5, 50.0)
        game8 = self.get_or_create_game(arya, strategy_cat, default_url, 80.0,
                                        'The Battle of the Bastards 8',
                                        default_desc, 4.5, 60.0)
        game9 = self.get_or_create_game(arya, fps_cat, default_url, 90.0,
                                        'The Battle of the Bastards 9',
                                        default_desc, 4.5, 70.0)
        game10 = self.get_or_create_game(jon, fps_cat, default_url, 100.0,
                                         'The Battle of the Bastards 10',
                                         default_desc, 4.5, 80.0)
        bran.games.add(game1, game3, game5, game7, game9)
        robb.games.add(game2, game4, game6, game8, game10)
        ned.games.add(game1, game5, game10)
