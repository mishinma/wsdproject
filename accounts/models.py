from django.contrib.auth.models import User
from community.models import Game


# Create your models here.

class UserMethods(User):

    def plays_game(self, game):
        return self.games.filter(id=game.id).exists()

    def develops_game(self, game):
        return game.developer.id == self.id

    class Meta:
        proxy = True
