
import django.contrib.auth.views as auth_views

from django.conf.urls import url
from accounts import views

app_name = 'accounts'

urlpatterns = [
    url('^register/$', views.register, name='register-user'),
    url('^login/$', auth_views.login, {'template_name': 'accounts/login-form.html'},
        name='login-user'),
    url('^logout/$', auth_views.logout, name='logout-user')
]

