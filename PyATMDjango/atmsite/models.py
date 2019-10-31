from django.db import models
from django.utils import timezone
from datetime import timedelta
import hashlib


# Create your models here.
class Account(models.Model):
    account_hash = models.CharField(max_length=32, null=True)
    login_time = models.DateTimeField(default=timezone.now())
    logged_in = models.BooleanField(default=True)
    account_number = models.IntegerField()
    phone_number = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    balance = models.FloatField(default=0)
    address = models.CharField(max_length=100)

    def tryhash(self):
        # Assert essential fields are non-null except account_hash
        if all(map(lambda v: v is not None, [self.account_number, self.phone_number, self.username,
                                         self.password, self.balance, self.address])):
            a_hash = hashlib.sha3_256(bytes(self.username, 'utf-8'))
            self.account_hash = a_hash.hexdigest()
            return True
        else:
            return False


    def time_expired(self):
        return (timezone.now() - self.login_time) > timedelta(hours=2)

    def __str__(self):
        return self.username


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.IntegerField(default=0)
    pin = models.IntegerField()
    date_issued = models.DateTimeField()
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=8, default="Active")

    def is_valid(self):
        # Assert essential fields are non-null except account_hash
        return all(map(lambda v: v is not None, [self.account, self.card_number, self.pin,
                                         self.expiry_date, self.date_issued]))

    def __str__(self):
        return self.card_number

