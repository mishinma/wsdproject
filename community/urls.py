from django.conf.urls import url
from community import views

app_name = 'community'

urlpatterns = [
    url(r'^games/(?P<game_id>\d+)/$', views.game_info, name='game-info'),
    url(r'^games/(?P<game_id>\d+)/play/$', views.play_game, name='game-play'),
    url(r'^games/(?P<game_id>\d+)/edit/$', views.edit_game, name='game-edit'),
    url(r'^games/my-inventory/$', views.my_inventory, name='my-inventory'),
    url(r'^games/create/$', views.create_game, name='game-create'),
]
