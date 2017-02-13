from django.contrib.auth.models import User
from community.models import Game


# Create your models here.

class UserMethods(User):

    def owns_game(self, game_id):
        return self.games.filter(id=game_id).exists()

    class Meta:
        proxy = True
