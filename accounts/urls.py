
import django.contrib.auth.views as auth_views

from django.conf.urls import url
from accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.register, name='register-user'),
    url(r'^register/activate', views.registration_complete, name='registration-complete'),
    url(r'^register/success', views.registration_success, name='registration-success'),
    url(r'^login/$', views.login, name='login-user'),
    url('^logout/$', auth_views.logout, name='logout-user')
]
