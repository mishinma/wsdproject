from django import forms
from community.models import Game


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = '__all__'
