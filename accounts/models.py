from django.contrib.auth.models import User
from community.models import Game


# Create your models here.

class UserMethods(User):
    def owns_game(self, game_id):
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return False
        else:
            return game.players.filter(id=self.id).exists()

    class Meta:
        proxy = True
