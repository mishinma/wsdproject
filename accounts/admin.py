from django.contrib import admin

# Register your models here.

from community.models import Game, GameCategory

admin.site.register([Game, GameCategory])
