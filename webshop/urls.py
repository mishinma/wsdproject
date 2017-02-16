from django.conf.urls import url

from webshop import views

app_name = 'webshop'

urlpatterns = [
    url(r'^shop/buy/(?P<game_id>\d+)/$', views.purchase_game, name='purchase-game'),
    url(r'^shop/buy/pending/$', views.purchase_pending, name='purchase-pending'),
    url(r'^shop/buy/callback', views.purchase_callback, name='purchase-callback'),
]
