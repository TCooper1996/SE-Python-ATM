from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from random import randint
import re

username_pattern = "^[a-zA-Z].{5,19}"
password_pattern = "(?=.*[!@#$%^&*])[0-9a-zA-Z!@#$%]{8,20}"
phone_pattern = "[0-9]{10}"
address_pattern = ".+"

from .models import Account, Card


# Create your views here.
def index(request):
    response = render(request, "atmsite/index.html")
    if request.COOKIES.get('current_account'):
        response.delete_cookie('current_account')
    return response


def create_account(request):
    return render(request, 'atmsite/create_account.html')


def view_balance(request):
    return HttpResponse("View account balance")


def account_menu(request):
    current_account_id = request.COOKIES.get('current_account')
    if not current_account_id:
        return HttpResponseRedirect(reverse('index'))
    else:
        a = Account.objects.get(id=current_account_id)
        return render(request, 'atmsite/account_menu.html', {"account": a})


def deposit(request):
    return render(request, 'atmsite/deposit.html')


def deposit_post(request):
    return HttpResponse('Deposit post not yet implemented')


def withdraw(request):
    return render(request, 'atmsite/withdraw.html')


def withdraw_post(request):
    # Get currently logged in user, or redirect to log in if there is none.
    if request.COOKIES.get('current_account'):
        a = Account.objects.get(id=request.COOKIES.get('current_account'))
    else:
        return HttpResponseRedirect(reverse('index'))

    # Get amount submitted, or reload page with error message if amount is empty string.
    try:
        amount = int(request.POST['amount'])
        # Raise ValueError if amount is not divisible by 20
        if amount % 20 != 0:
            raise ValueError
    except ValueError:
        return render(request, 'atmsite/withdraw.html',
                      {'errors': ['Please enter an integer amount divisible by $20 in the textbox.']})

    errors = []
    if a.balance > amount:
        a.balance -= amount
        a.save()
        return HttpResponseRedirect(reverse('account_menu'))
    else:
        errors.append("Insufficient funds. Your balance currently stands at {:.2f}".format(a.balance))
        return render(request, 'atmsite/withdraw.html', {'errors': errors})


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
        if Account.objects.get(username__exact=name):
            errors.append("ERROR: Username is taken.")

        # Branch if no error recorded
        if not errors:
            account = Account(username=name, password=password, phone_number=phone, address=address)
            account.account_number = randint(0, 10000)
            account.save()
            return HttpResponseRedirect(reverse('account_menu'))

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
            response = HttpResponseRedirect(reverse('account_menu'))
            response.set_cookie('current_account', a.id)
            return response
        else:
            return render(request, 'atmsite/index.html', {'error': 'Unknown or Incorrect username/password'})

    except IndexError:
        return render(request, 'atmsite/index.html', {'error': 'Unknown or Incorrect username/password'})