from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Stock, Wallet

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker","quantity"]

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["balance"]

