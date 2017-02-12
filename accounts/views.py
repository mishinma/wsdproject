from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group


def register_player(request):
    form, new_user = get_user_from_registration_form(request)
    if new_user is not None:
        # user.password refers to password hash
        player_group = Group.objects.get(name='player')
        new_user.groups.add(player_group)
        new_user.save()
        password = form.cleaned_data['password']
        user = authenticate(username=new_user.username, password=password)
        if user is not None and user.is_active:
                login(request, user)
                return render(request, 'community/welcome_user.html', {'games': None})
    context = {
        "form": form,
    }
    return render(request, 'accounts/registration_form.html', context)


def register_devloper(request):
    form, new_user = get_user_from_registration_form(request)
    if new_user is not None:
        # user.password refers to password hash
        developer_group = Group.objects.get(name='developer')
        new_user.groups.add(developer_group)
        new_user.save()
        password = form.cleaned_data['password']
        user = authenticate(username=new_user.username, password=password)
        if user is not None and user.is_active:
                login(request, user)
                return render(request, 'community/welcome_user.html', {'games': None})
    context = {
        "form": form,
    }
    return render(request, 'accounts/registration_form.html', context)


def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'community/welcome_user.html', {'games': None})
    context = {
        'form': form,
    }
    return render(request, 'accounts/login_form.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')


def get_user_from_registration_form(request):
    form = RegistrationForm(request.POST or None)
    new_user = None
    if form.is_valid():
        new_user = form.save(commit=False)
        password = form.cleaned_data['password']
        new_user.set_password(password)
        new_user.save()
    return form, new_user
