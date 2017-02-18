from django import forms
from community.models import Game
from decimal import Decimal


class GameForm(forms.ModelForm):

    #ToDo: Prefix URL's with http://

    class Meta:
        model = Game
        fields = ['name', 'source_url', 'category', 'description',
                  'price', 'sales_price', 'logo']

    def clean_sales_price(self):
        sales_price = None
        if self.data['sales_price']:
            sales_price = Decimal(self.data['sales_price'])
            price = Decimal(self.cleaned_data['price'])
            if sales_price >= price:
                raise forms.ValidationError('Sales price cannot be higher than normal price')
        return sales_price
