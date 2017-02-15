from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models import Max


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

    objects = GameManager()

    def get_user_high_score(self, user):
        high_score = self.game_score_set.filter(player=user).order_by('-score').first()
        high_score_value = high_score.score if high_score is not None else None
        return high_score_value

    def get_user_last_score(self, user):
        last_score = self.game_score_set.filter(player=user).order_by('-timestamp').first()
        last_score_value = last_score.score if last_score is not None else None
        return last_score_value

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
