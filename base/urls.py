from django.conf.urls import url
from . import views

app_name = 'base'

urlpatterns = [

    url(r'^index/$', views.index, name='index'),  # default homepage
]
