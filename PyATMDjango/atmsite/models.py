from django.db import models
from django.utils import timezone
from datetime import timedelta
import hashlib


# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=100)
    balance = models.FloatField(default=0)
    login_time = models.DateTimeField(default=timezone.now)
    account_number = models.IntegerField()

    def __str__(self):
        return self.username


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.IntegerField(default=0)
    pin = models.IntegerField()
    date_issued = models.DateField()
    expiry_date = models.DateField()
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=100)

    def is_valid(self):
        # Assert essential fields are non-null except account_hash
        return all(map(lambda v: v is not None, [self.account, self.card_number, self.pin,
                                         self.expiry_date, self.date_issued]))

    def __str__(self):
        return str(self.card_number)


def get_next_maintenance_date():
    return timezone.now() + timedelta(weeks=104)


class ATM(models.Model):
    current_balance = models.FloatField(default=0)
    current_location = models.CharField(max_length=50)
    minimum_balance = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    last_refill_date = models.DateTimeField(default=timezone.now)
    next_maintenance_date = models.DateTimeField(default=get_next_maintenance_date)


class Transaction(models.Model):
    card_number = models.IntegerField()
    atm = models.ForeignKey(ATM, on_delete=models.CASCADE)
    date = models.DateTimeField(timezone.now)

    def get_date(self):
        return self.date.strftime('%d/%m/%Y')

    def __str__(self):
        return "{} with atm {} on {}".format(str(self.card_number), self.atm, self.get_date())


class CashTransfer(Transaction):
    receiving_account_number = models.IntegerField()
    receiving_account_name = models.IntegerField()
    amount_transferred = models.FloatField()

    def __str__(self):
        return "{} sent to {}".format(self.amount_transferred, self.receiving_account_name)


class BalanceEnquiry(Transaction):
    def __str__(self):
        return "Balance viewed"


class CashWithdrawal(Transaction):
    amount_transferred = models.FloatField()
    current_balance = models.FloatField()

    def __str__(self):
        return "{} was withdrawn, resulting in a balance of {}".format(self.amount_transferred, self.current_balance)


class PinChange(Transaction):
    previous_pin = models.IntegerField()
    next_pin = models.IntegerField()

    def __str__(self):
        return "Pin was updated"


class PhoneNumberChange(Transaction):
    phone_number = models.IntegerField()

    def __str__(self):
        return "Phone number was updated to {}".format(self.phone_number)
