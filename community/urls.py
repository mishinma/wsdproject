from django.conf.urls import url
from community import views

app_name = 'community'

urlpatterns = [
    url(r'^games/(?P<game_id>[0-9]+)/$', views.game_info, name='game_info'),
]
