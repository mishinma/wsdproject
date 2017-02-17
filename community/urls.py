from django.conf.urls import url
from community import views

app_name = 'community'

urlpatterns = [
    url(r'^games/(?P<game_id>\d+)/$', views.game_info, name='game-info'),
    url(r'^games/(?P<game_id>\d+)/play/$', views.play_game, name='game-play'),
    url(r'^games/(?P<category>\w+)/$', views.search_by_category, name='search-category'),
    url(r'^games/search', views.search_by_query, name='search-query'),
    url(r'^my-games/$', views.my_games, name='my-games'),
    url(r'^dev/games/(?P<game_id>\d+)/edit/$', views.edit_game, name='game-edit'),
    url(r'^dev/my-inventory/$', views.my_inventory, name='my-inventory'),
    url(r'^dev/games/create/$', views.create_game, name='game-create'),
]
