from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class Developer(models.Model):
    developer_id = models.OneToOneField(User, on_delete=models.CASCADE)
    corp_page = models.fields.URLField()


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.fields.CharField(max_length=50, unique=True)


class Game(models.Model):
    # Use unique slug for game URL?
    game_id = models.fields.SlugField(unique=True, primary_key=True)
    developer_id = models.ForeignKey(Developer)  # Should this be cascading?
    category_id = models.ForeignKey(Category)
    source_url = models.fields.URLField()
    price = models.fields.DecimalField(decimal_places=2,
                                       validators=[MinValueValidator(0.0)])
    name = models.fields.CharField(max_length=50)
    description = models.fields.TextField(blank=True)
    game_logo = models.ImageField(null=True)  # Should specify height and width
    rating = models.fields.FloatField(validators=[MinValueValidator(0.0),
                                                  MaxValueValidator(5.0)])


class Player(models.Model):
    player_id = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, symmetrical=False, null=True)


class Game_Score(models.Model):
    category_id = models.AutoField(primary_key=True)
    # Cascading?
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    score = models.fields.BigIntegerField(null=False,
                                          validators=[MinValueValidator(0)])
    timestamp = models.DateTimeField(default=timezone.now())


class Game_State(models.Model):
    state_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    state_data = JSONField()
    timestamp = models.DateTimeField(default=timezone.now())
    # name = models.fields.CharField(max_length=50)


class Transaction(models.Model):
    # Should the length be fixed?
    pid = models.fields.CharField(max_length=100, primary_key=True)
    ref = models.fields.CharField(max_length=100)
    amount = models.fields.DecimalField(decimal_places=2,
                                        validators=[MinValueValidator(0.0)])
    result = models.fields.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now())


class Gift(models.Model):
    gift_id = models.AutoField(primary_key=True)
    receiver = models.ForeignKey(Player)
    message = models.fields.TextField(blank=True)


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Transaction)
    payer = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    gift_id = models.ForeignKey(Gift, null=True)
