from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import randint
import re
username_pattern = "^[a-zA-Z].{5,19}"
password_pattern = "(?=.*[!@#$%^&*])[0-9a-zA-Z!@#$%]{8,20}"
phone_pattern = "[0-9]{10}"
address_pattern = ".+"

from .models import Account, Card


# Create your views here.
def index(request):
    return render(request, "atmsite/index.html")


def create_account(request):
    return render(request, 'atmsite/create_account.html')


def view_balance(request, account_hash):
    return HttpResponse("View account balance")


def account_menu(request, account_hash):
    for a in Account.objects.all():
        if a.account_hash == account_hash:
            return render(request, 'atmsite/account_menu.html', {"account": a})


# This view should validate account creation and redirect user to their account menu if it is valid,
# Otherwise reload the acount creation page with the correct error message
def create_account_post(request):
    errors = []
    try:
        name = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']

        # Anonymous function that returns true if the given val fails to match the regex pattern, pat
        re_fails = lambda pat, val: re.search(pat, val) is None

        if re_fails(username_pattern, name):
            errors.append("ERROR: Username must begin with a letter and be at least 6 characters long.")
        if re_fails(password_pattern, password):
            errors.append("ERROR: Password must be 8 and 20 characters and contain at least one character from [!@#$%^&*]")
        if re_fails(phone_pattern, phone):
            errors.append("ERROR: Phone number must be numeric and be between 10 characters long.")
        if re_fails(address_pattern, address):
            errors.append("ERROR: Address field is required.")
        if name in [a.username for a in Account.objects.all()]:
            errors.append("ERROR: Username is taken.")

        # Branch if no error recorded
        if not errors:
            account = Account(username=name, password=password, phone_number=phone, address=address)
            account.account_number = randint(0, 10000)
            account.save()
            return HttpResponseRedirect(reverse('account_menu', args=[account.account_hash]))

        # Branch if an error was recorded, reload account creation page
        else:
            return render(request, 'atmsite/create_account.html', {'errors': errors})

    except KeyError:
        return render(request, 'atmsite/create_account.html', {'errors': errors})


# This view is called after the log in form is submitted from the index page.
# The given username and password must be authenticated
def authenticate_account(request):
    try:
        name = request.POST['username']
        password = request.POST['password']
        a = Account.objects.filter(username__exact=name)[0]
        if a.password == password:
            return HttpResponseRedirect(reverse('account_menu', args=[a.account_hash]))
        else:
            return render(request, 'atmsite/index.html', {'error': 'Unknown or Incorrect username/password'})

    except IndexError:
        return render(request, 'atmsite/index.html', {'error': 'Unknown or Incorrect username/password'})