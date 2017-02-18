from django import forms
from community.models import Game


class GameForm(forms.ModelForm):

    #ToDo: Prefix URL's with http://

    class Meta:
        model = Game
        fields = ['name', 'source_url', 'category', 'description',
                  'price', 'sales_price', 'logo']

    def clean_sales_price(self):
        sales_price = self.data['sales_price']
        if sales_price and sales_price >= self.data['price']:
            raise forms.ValidationError('Sales price cannot be higher than normal price')
        return self.data['sales_price']
