
import django.contrib.auth.views as auth_views

from django.conf.urls import url
from accounts import views

app_name = 'accounts'

urlpatterns = [
    url('^register/$', views.register, name='register_user'),
    url('^login/$', auth_views.login, {'template_name': 'accounts/login_form.html'}, name='login_user'),
    url('^logout/$', auth_views.logout, name='logout_user')
]

