from django.conf.urls import url
from . import views

app_name = 'community'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),  #default homepage

]