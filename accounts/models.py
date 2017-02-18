from django.contrib.auth.models import User
from django.db import models
from hashlib import md5
from haze.settings import SECRET_KEY

import time
import urllib.parse


# Create your models here.

class UserMethods(User):

    def plays_game(self, game):
        return self.games.filter(id=game.id).exists()

    def develops_game(self, game):
        return game.developer.id == self.id

    def confirmed(self):
        return self.emailconfirmed.email_confirmed

    class Meta:
        proxy = True


class EmailConfirmed(models.Model):
    user = models.OneToOneField(User)
    email_confirmed = models.fields.BooleanField(default=False)


class PendingRegistrationManager(models.Manager):

    def create_new_pending(self, user, base_url):
        timestamp = int(time.time())
        link = self.generate_link(user, timestamp, base_url)

        PendingRegistration(
            user=user,
            link=link,
            timestamp=timestamp
        ).save()

        EmailConfirmed.objects.create(user=user)

        return link

    def generate_link(self, user, timestamp, base_url):
        token_str = "username={}&email={}&timestamp={}&secret_key={}".format(
            user.username,
            user.email,
            timestamp,
            SECRET_KEY
        )

        token = md5(token_str.encode('ascii')).hexdigest()
        params = urllib.parse.urlencode({
            'id': user.id,
            'token': token
        })

        return '{}?{}'.format(base_url, params)


class PendingRegistration(models.Model):
    user = models.OneToOneField(User)
    link = models.fields.URLField()
    timestamp = models.IntegerField()

    objects = PendingRegistrationManager()

    def verfify_token(self, token):
        checksum_str = "username={}&email={}&timestamp={}&secret_key={}".format(
            self.user.username,
            self.user.email,
            self.timestamp,
            SECRET_KEY
        )
        checksum = md5(checksum_str.encode('ascii')).hexdigest()

        return checksum == token
