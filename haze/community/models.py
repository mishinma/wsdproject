from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Developer, Player


class Game_Category(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)


class Game(models.Model):
    # Use unique slug for game URL?
    slug = models.fields.SlugField(unique=True)
    developer = models.ForeignKey(Developer)  # Should this be cascading?
    category = models.ForeignKey(Game_Category)
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
    rating = models.fields.FloatField(validators=[MinValueValidator(0.0),
                                                  MaxValueValidator(5.0)])


class Game_Score(models.Model):
    # Cascading?
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    score = models.fields.BigIntegerField(validators=[MinValueValidator(0)])
    timestamp = models.DateTimeField(default=timezone.now)


class Game_State(models.Model):
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    state_data = JSONField()
    timestamp = models.DateTimeField(default=timezone.now)
    # name = models.fields.CharField(max_length=50)
