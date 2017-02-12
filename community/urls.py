from django.conf.urls import url
from community import views

app_name = 'community'

urlpatterns = [
    url(r'^games/(?P<game_id>\d+)/$', views.game_info, name='game-info'),
    url(r'^games/(?P<game_id>\d+)/play/$', views.play_game, name='game-play')
]
