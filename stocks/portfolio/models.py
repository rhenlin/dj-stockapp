from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0, blank=False)
  
    def __str__(self):
        return self.ticker

class Wallet(models.Model):
    balance = models.IntegerField()
