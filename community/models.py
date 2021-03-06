from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models import Max

ACTION_BUY = 'buy'
ACTION_PLAY = 'play'
ACTION_DEVELOP = 'develop'

class GameCategory(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<GameCategory: {}>".format(self.name)

    class Meta:
        verbose_name_plural = 'game_categories'


class GameManager(models.Manager):

    def games_for_developer(self, developer):
        """ Return a queryset of games that `developer` develops """
        return super(GameManager, self).get_queryset().filter(developer=developer)

    def games_for_player(self, player):
        """ Return a queryset of games that `player` plays in """
        return super(GameManager, self).get_queryset().filter(players__id=player.id)

    @staticmethod
    def add_action_single(game, user):
        if not user.is_authenticated():
            game.action = ACTION_BUY
        elif user.is_player():
            if user.plays_game(game):
                game.action = ACTION_PLAY
            else:
                game.action = ACTION_BUY
        elif user.is_developer():
            if user.develops_game(game):
                game.action = ACTION_DEVELOP
            else:
                game.action = None
        else:
            game.action = None

        return game


    @staticmethod
    def add_action(games, user):
        games_w_actions = []
        if not user.is_authenticated():
            for game in games:
                game.action = ACTION_BUY
                games_w_actions.append(game)
        elif user.is_player():
            for game in games:
                if user.plays_game(game):
                    game.action = ACTION_PLAY
                else:
                    game.action = ACTION_BUY
                games_w_actions.append(game)
        elif user.is_developer():
            for game in games:
                if user.develops_game(game):
                    game.action = ACTION_DEVELOP
                else:
                    game.action = None
                games_w_actions.append(game)
        else:
            for game in games:
                game.action = None
                games_w_actions.append(game)

        return games_w_actions


class Game(models.Model):
    # Use unique slug for game URL?
    slug = models.fields.SlugField(unique=True)
    developer = models.ForeignKey(User)  # Should this be cascading?
    players = models.ManyToManyField(User, related_name='games')
    category = models.ForeignKey(GameCategory)
    source_url = models.fields.URLField()
    price = models.fields.DecimalField(max_digits=5,
                                       decimal_places=2,
                                       validators=[MinValueValidator(0.0),
                                                   MaxValueValidator(999.99)])
    sales_price = models.fields.DecimalField(max_digits=5, decimal_places=2,
                                             validators=[MinValueValidator(0.0),
                                                         MaxValueValidator(999.99)],
                                             null=True, blank=True)
    name = models.fields.CharField(max_length=50, unique=True)
    description = models.fields.TextField(blank=True)
    logo = models.ImageField(null=True, blank=True)  # Should specify height and width
    rating = models.fields.DecimalField(max_digits=2,
                                        decimal_places=1,
                                        validators=[MinValueValidator(0.0),
                                                    MaxValueValidator(5.0)])

    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    objects = GameManager()

    def get_user_high_score(self, user):
        high_score = self.gamescore_set.filter(player=user).order_by('-score').first()
        high_score_value = high_score.score if high_score is not None else None
        return high_score_value

    def get_user_last_score(self, user):
        last_score = self.gamescore_set.filter(player=user).order_by('-timestamp').first()
        last_score_value = last_score.score if last_score is not None else None
        return last_score_value

    def get_user_last_state(self, user):
        return self.gamestate_set.filter(player=user).order_by('-timestamp').first()

    def get_top_scores(self, n):
        return self.gamescore_set.order_by('-score')[:n]

    def get_price(self):
        """ Check if the game is on sale and return the price """
        return self.price if not self.sales_price else self.sales_price

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Game: {}>".format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Game, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        permissions = (
            ("play_game", "Can play the game"),
            ("test_game", "Can test games"),
            ("buy_game", "Can buy games")
        )


class GameScore(models.Model):
    # Cascading?
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    score = models.fields.BigIntegerField(validators=[MinValueValidator(0)])
    timestamp = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return "<GameScore: game={}, score={}>, time={}".format(self.game.id, self.score, self.timestamp)


class GameState(models.Model):
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    state_data = JSONField()
    timestamp = models.DateTimeField(default=timezone.now)

    # name = models.fields.CharField(max_length=50)

    def __repr__(self):
        return '<GameState: game={}, player={} state={}, time={}>'.format(
            self.game.id, self.player.username, self.state_data, self.timestamp)
