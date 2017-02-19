from django.conf.urls import url
from api import views

app_name = 'api'

urlpatterns = [
    url(r'^api/v1/games/cat/(?P<category>\w+)/$', views.get_games_of_category, name='cat-games'),
    url(r'^api/v1/games/dev/(?P<dev_id>\d+)/$', views.get_games_of_dev, name='dev-games'),
    url(r'^api/v1/games/(?P<game_id>\d+)/$', views.get_game_detail, name='game-detail'),
    url(r'^api/v1/games/(?P<game_id>\d+)/scores/$', views.get_scores_of_game, name='game-scores'),
    url(r'^api/v1/categories/$', views.get_categories, name='all-cats'),
    url(r'^api/v1/devs/$', views.get_developers, name='all-devs'),
]
