from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Developer(models.Model):
    developer_id = models.OneToOneField(User, on_delete=models.CASCADE)
    corp_page = models.fields.URLField()


class Player(models.Model):
    player_id = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField('community.Game', symmetrical=False)
    games = models.fields.TextField()
