from django.conf.urls import url

from webshop import views

app_name = 'webshop'

urlpatterns = [
    url(r'^shop/buy/(?P<game_id>\d+)/$', views.purchase_game, name='purchase-game'),
    url(r'^shop/buy/success', views.success, name='purchase-success'),
    url(r'^shop/buy/cancel', views.cancel, name='purchase-cancel'),
    url(r'^shop/buy/error', views.error, name='purchase-error'),
]
