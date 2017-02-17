from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views import defaults

from accounts.models import PendingRegistration, UserMethods


def register(request):

    if request.user.is_authenticated():
        return redirect('base:index')

    if request.POST:
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()

            # Add `new_user` to a group
            if form.cleaned_data['is_developer']:
                user_group = Group.objects.get(name='developer')
            else:
                user_group = Group.objects.get(name='player')
            new_user.groups.add(user_group)
            new_user.save()

            # # Log in the user
            # auth_user = authenticate(username=new_user.username, password=password)
            # if auth_user is not None:
            #     login(request, auth_user)
            #     return redirect('base:index')
            base_url = request.build_absolute_uri(
                reverse('accounts:registration-complete')
            )

            verification_link = PendingRegistration.objects.create_new_pending(
                user=new_user,
                base_url=base_url
            )
            print(verification_link)
            return redirect('base:index')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration-form.html', context={'form': form})


def registration_complete(request):
    try:
        user_id = request.GET['id']
        token = request.GET['token']
    except KeyError:
        return defaults.bad_request(request=request, exception=KeyError)

    user = get_object_or_404(UserMethods, id=user_id)
    pending_registration = get_object_or_404(PendingRegistration, user=user)

    if pending_registration.verfify_token(token):
        return redirect('base:index')
    else:
        return defaults.bad_request(request=request, exception=SuspiciousOperation)
