from django import forms
from community.models import Game


class GameForm(forms.ModelForm):

    #ToDo: Prefix URL's with http://

    class Meta:
        model = Game
        fields = ['name', 'source_url', 'category', 'description',
                  'price', 'sales_price', 'logo']
