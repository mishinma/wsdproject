from django.conf.urls import url

app_name = 'community'

urlpatterns = [
    url(r'^$', views.index, name='index'),  #default homepage
    url(r'^(?P<game_id>[0-9]+)/$', views.game_info, name='game_info'),
]
