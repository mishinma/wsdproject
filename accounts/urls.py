from django.conf.urls import url
from accounts import views

app_name = 'accounts'

urlpatterns = [
    url('^register/', views.register_player, name='register-user'),
    url('^login/', views.login_user, name='login-user'),

]
