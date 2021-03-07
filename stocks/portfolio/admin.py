from django.contrib import admin
from .models import Stock, Wallet

# Register your models here.
admin.site.register(Stock)
admin.site.register(Wallet)