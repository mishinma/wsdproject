from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group


def register(request):
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

            # Log in the user
            auth_user = authenticate(username=new_user.username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return render(request, 'community/welcome_user.html', {'games': None})
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration_form.html', context={'form': form})

