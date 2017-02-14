from django import forms
from accounts.models import UserMethods
from webshop.models import PendingTransaction


class PaymentForm(forms.Form):
    is_gift = forms.BooleanField(label="Send as gift", required=False)
    gift_recipient = forms.ModelChoiceField(queryset=[], empty_label=None, to_field_name='username',
                                            label='Gift to')
    pid = forms.CharField(max_length=100, widget=forms.HiddenInput())
    sid = forms.CharField(max_length=100, widget=forms.HiddenInput())
    amount = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.HiddenInput())
    success_url = forms.CharField(max_length=150, widget=forms.HiddenInput())
    cancel_url = forms.CharField(max_length=150, widget=forms.HiddenInput())
    error_url = forms.CharField(max_length=150, widget=forms.HiddenInput())
    checksum = forms.CharField(max_length=150, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.payer_id = kwargs.pop('payer_id')
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['gift_recipient'].queryset = UserMethods.objects.filter(groups__name='player').exclude(id=self.payer_id)


class PendingTransactionForm(forms.ModelForm):
    pid = forms.CharField(max_length=100, widget=forms.HiddenInput())
    sid = forms.CharField(max_length=100, widget=forms.HiddenInput())
    amount = forms.DecimalField(max_digits=5, decimal_places=2,
                                widget=forms.HiddenInput)
    success_url = forms.CharField(max_length=150, widget=forms.HiddenInput())
    cancel_url = forms.CharField(max_length=150, widget=forms.HiddenInput())
    error_url = forms.CharField(max_length=150, widget=forms.HiddenInput())
    checksum = forms.CharField(max_length=150, widget=forms.HiddenInput())

    class Meta:
        model = PendingTransaction
        fields = ['pid']
