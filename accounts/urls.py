
import django.contrib.auth.views as auth_views

from django.conf.urls import url
from accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.register, name='register-user'),
    url(r'^register/success', views.registration_complete, name='registration-complete'),
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login-form.html'},
        name='login-user'),
    url('^logout/$', auth_views.logout, name='logout-user')
]
