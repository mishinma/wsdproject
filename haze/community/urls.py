from django.conf.urls import url
from community import views

app_name = 'community'

urlpatterns = [
    url(r'^$', views.index, name='index'),  #default homepage
    url(r'^games/(?P<id>[0-9]+)/$', views.game_info, name='game_info'),
]
