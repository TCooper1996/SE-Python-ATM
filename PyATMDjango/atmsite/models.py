from django.db import models


# Create your models here.
class Account(models.Model):
    account_number = models.IntegerField(default=0)
    phone_number = models.IntegerField(default=0)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    balance = models.FloatField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.IntegerField(default=0)
    pin = models.IntegerField()
    date_issued = models.DateTimeField()
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=8)

    def __str__(self):
        return self.card_number

