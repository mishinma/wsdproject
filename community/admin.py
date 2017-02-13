from django.contrib import admin

# Register your models here.

from community.models import Game, Game_Category

admin.site.register([Game, Game_Category])