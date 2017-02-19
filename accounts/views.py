from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login as default_login
from django.urls import reverse
from django.views import defaults
from django.core import mail
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from accounts.models import PendingRegistration, UserMethods, EmailConfirmed
from accounts.forms import RegistrationForm, EditProfileForm, ChangePasswordForm

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

            base_url = request.build_absolute_uri(
                reverse('accounts:registration-complete')
            )

            verification_link = PendingRegistration.objects.create_new_pending(
                user=new_user,
                base_url=base_url
            )
            send_email(new_user, verification_link)
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
        record = EmailConfirmed.objects.get(user=user)
        record.email_confirmed = True
        record.save()
        PendingRegistration.objects.filter(user=user).delete()
        return redirect('accounts:registration-success')
    else:
        return defaults.bad_request(request=request, exception=SuspiciousOperation)


def registration_success(request):
    return render(request, 'accounts/registration-success.html')


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if UserMethods.objects.filter(username=username).exists():
            user = UserMethods.objects.get(username=username)
            if user.check_password(password) and not user.confirmed():
                    form = AuthenticationForm(data=request.POST)
                    form.add_error(None, 'Please confirm your email address before trying to log in')
                    context = {
                        'form': form
                    }
                    return render(request, 'accounts/login-form.html', context=context)

    return default_login(request, template_name='accounts/login-form.html')


def send_email(user, link):
    mail_template = get_template('accounts/activation-email.html')
    d = Context({
        'username': user.username,
        'url': link,
    })

    body = mail_template.render(d)

    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject='Account activation',
            body=body,
            from_email='registration@haze.com',
            to=[user.email],
            connection=connection,
        ).send()


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(data=request.POST)
        user = request.user
        new_username = request.POST['new_username']
        new_email = request.POST['new_email']
        password = request.POST['password']
        if not user.check_password(password):
            form.add_error(None, 'Please provide correct password to apply changes.')

        if form.is_valid():
            if new_username:
                user.username = new_username
            if new_email:
                user.email = new_email
            user.save()
            return redirect('base:index')

    else:
        form = EditProfileForm()
    return render(request, 'accounts/edit-account-form.html', context={'form': form})


def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST)
        user = request.user
        new_password = request.POST['new_password']
        current_password = request.POST['current_password']
        if not user.check_password(current_password):
            form.add_error(None, 'Please provide correct password to apply changes.')

        if form.is_valid():
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('base:index')
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/change-password-form.html', context={'form': form})


@sensitive_post_parameters()
@csrf_protect
@never_cache
def delete_profile(request):
    user = request.user
    form = AuthenticationForm(data=request.POST)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username != user.username:
            form.add_error(None, 'Please provide your username to delete your account')
        if not user.check_password(password):
            form.add_error(None, 'Please confirm your email address to delete your account')
        if form.is_valid():
            request.user.is_active = False
            request.user.save()
            logout(request)
            return redirect('base:index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/delete-profile-form.html', context={'form': form})