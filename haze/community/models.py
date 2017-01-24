from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Developer(models.Model):
    developer_id = models.OneToOneField(User, on_delete=models.CASCADE)
    corp_page = models.fields.URLField()


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.fields.CharField(max_length=50, unique=True)


class Game(models.Model):
    # Use unique slug for game URL?
    game_id = models.AutoField(primary_key=True)
    game_slug = models.fields.SlugField(unique=True, primary_key=True)
    developer_id = models.ForeignKey(Developer)  # Should this be cascading?
    category_id = models.ForeignKey(Category)
    source_url = models.fields.URLField()
    price = models.fields.DecimalField(max_digits=5,
                                       decimal_places=2,
                                       validators=[MinValueValidator(0.0)],
                                                   MaxValueValidator(999.99))
    sales_price = models.fields.DecimalField(max_digits=5, decimal_places=2,
                                             validators=[MinValueValidator(0.0),
                                                         MaxValueValidator(999.99)],
                                             null=True)
    name = models.fields.CharField(max_length=50, unique=True)
    description = models.fields.TextField(blank=True)
    game_logo = models.ImageField(null=True)  # Should specify height and width
    rating = models.fields.FloatField(validators=[MinValueValidator(0.0),
                                                  MaxValueValidator(5.0)])


class Player(models.Model):
    player_id = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, symmetrical=False)


class Game_Score(models.Model):
    category_id = models.AutoField(primary_key=True)
    # Cascading?
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    score = models.fields.BigIntegerField(null=False,
                                          validators=[MinValueValidator(0)])
    timestamp = models.DateTimeField(default=timezone.now)


class Game_State(models.Model):
    state_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    state_data = JSONField()
    timestamp = models.DateTimeField(default=timezone.now)
    # name = models.fields.CharField(max_length=50)
