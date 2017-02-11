from django.conf.urls import url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

app_name = 'accounts'

urlpatterns = [
    url('^register/', CreateView.as_view(
            template_name='accounts/registration_form.html',
            form_class=UserCreationForm
    ), name='register-user'),

]
