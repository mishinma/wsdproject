from django.conf.urls import url
from api import views

app_name = 'accounts'

urlpatterns = [
    url(r'^api/v1/games/cat/(?P<category>\w+)/$', views.get_games_of_category),
    url(r'^api/v1/games/dev/(?P<dev_id>\d+)/$', views.get_games_of_dev),
    url(r'^api/v1/games/(?P<game_id>\d+)/$', views.get_game_detail),
    url(r'^api/v1/games/(?P<game_id>\d+)/scores/$', views.get_scores_of_game),
]
