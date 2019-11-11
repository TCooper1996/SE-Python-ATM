from django.contrib import admin

# Register your models here.
from .models import Account, ATM, Card

admin.site.register(Account)
admin.site.register(ATM)
admin.site.register(Card)
