from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_developer = forms.BooleanField(label="Sign up as developer",
                                      required=False)

    def clean_password(self):
        if self.data['password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords must match')
        return self.data['password']

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EditProfileForm(forms.ModelForm):
    new_username = forms.CharField(required=False)
    new_email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, help_text="Please provide password to apply changes")

    class Meta:
        model = User
        fields = ['new_username', 'new_email', 'password']


class ChangePasswordForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_new_password(self):
        if self.data['new_password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords must match')
        return self.data['new_password']

    class Meta:
        model = User
        fields = ['current_password','new_password']