from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['sender_account', 'receiver_account', 'amount','transaction_type']
