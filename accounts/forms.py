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
