from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from random import randint
import re
from datetime import datetime, date, timedelta

admin_password = "adminpass"

username_pattern = "^[a-zA-Z].{5,19}"
password_pattern = "(?=.*[!@#$%^&*\(\\)])[0-9a-zA-Z!@#$%\(\\)]{8,20}"
phone_pattern = "[0-9]+"
address_pattern = ".+"
card_number_pattern = "[0-9]{1,10}"
pin_pattern = "[0-9]{1,4}"

from .models import Account, Card, ATM

status_codes = {0: '', 1: "Transaction Succeeded", 2: "You are not logged in", 3: "Account created", 4: "Card Created",
                5: "Data saved"}


# Create your views here.
def index(request, status_code=0):
    response = render(request, "atmsite/index.html", {'status_code': status_codes[status_code]})

    if request.COOKIES.get('current_account'):
        response.delete_cookie('current_account')

    if request.COOKIES.get('admin'):
        response.delete_cookie('admin')

    return response


def admin_login(request):
    return render(request, "atmsite/admin_login.html")


def create_account(request):
    return render(request, 'atmsite/create_account.html')


def view_balance(request):
    current_account_id = request.COOKIES.get('current_account')
    if not current_account_id:
        return HttpResponseRedirect(reverse('index'), kwargs={'status_code': 2})
    else:
        a = Account.objects.get(id=current_account_id)
        return render(request, 'atmsite/view_balance.html', {"account": a})


def account_menu(request, status_code=0):
    current_account_id = request.COOKIES.get('current_account')
    if not current_account_id:
        return HttpResponseRedirect(reverse('index'))
    else:
        a = Account.objects.get(id=current_account_id)
        return render(request, 'atmsite/account_menu.html', {"account": a, "status_message": status_codes[status_code]})


def admin_menu(request, status_code=0):
    return render(request, 'atmsite/admin_menu.html', {"status_message": status_codes[status_code]})


def deposit(request):
    return render(request, 'atmsite/deposit.html')


def deposit_post(request):
    try:
        amount = int(request.POST['amount'])
    except ValueError:
        return render(request, 'atmsite/deposit.html',
                      {'errors': ['Please enter an integer amount in dollars. Coins are not accepted.']})

    # Get currently logged in user, or redirect to log in if there is none.
    if request.COOKIES.get('current_account'):
        a = Account.objects.get(id=request.COOKIES.get('current_account'))
    else:
        return HttpResponseRedirect(reverse('index'))

    a.balance += amount
    a.save()
    return HttpResponseRedirect(reverse('account_menu', kwargs={'status_code': 1}))


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
            errors.append("ERROR: Password must be 8 and 20 characters and contain at least one character in !@#$%^&*()")
        if re_fails(phone_pattern, phone):
            errors.append("ERROR: Phone number must be numeric.")
        if re_fails(address_pattern, address):
            errors.append("ERROR: Address field is required.")
        if Account.objects.filter(username__exact=name).exists():
            errors.append("ERROR: Username is taken.")

        # Branch if no error recorded
        if not errors:
            account = Account(username=name, password=password, phone_number=phone, address=address)
            account.account_number = randint(0, 10000)
            account.save()
            return HttpResponseRedirect(reverse('admin_menu', kwargs={'status_code': 3}))

        # Branch if an error was recorded, reload account creation page
        else:
            return render(request, 'atmsite/create_account.html', {'errors': errors})

    except KeyError:
        return render(request, 'atmsite/create_account.html', {'errors': errors})


def create_card(request):
    errors = []
    date = timezone.now().date().strftime("%Y-%m-%d")
    expiry_date = (timezone.now() + timedelta(weeks=104)).date().strftime("%Y-%m-%d")
    card_number = randint(0, 999999999)
    card_numbers = [card.card_number for card in Card.objects.all()]
    random_pin = randint(0, 9999)
    users = Account.objects.all()
    # Randomize card_number until a unique one is found.
    while card_number in card_numbers:
        card_number = randint(0, 999999999)
    return render(request, 'atmsite/create_card.html', {'errors': errors, 'current_date': date,
                                                        'expiry_date': expiry_date, 'random_card_number': card_number,
                                                        'users': users, 'random_pin': random_pin})


def create_card_post(request):
    errors = []
    try:
        name = request.POST['username']
        number = request.POST['number']
        pin = request.POST['pin']
        activation_date = datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
        expiry = datetime.strptime(request.POST['expiry'], "%Y-%m-%d").date()
        address = request.POST['address']
        balance = float(request.POST['balance'])
        phone = request.POST['phone']

        # Anonymous function that returns true if the given val fails to match the regex pattern, pat
        re_fails = lambda pat, val: re.search(pat, val) is None

        if not Account.objects.filter(username__exact=name).exists():
            errors.append("ERROR: User does not exist")
        if re_fails(card_number_pattern, number):
            errors.append("ERROR: Card number must be 1-10 digits")
        if re_fails(pin_pattern, pin):
            errors.append("ERROR: Phone number must be numeric long.")
        if activation_date < datetime.today().date():
            errors.append("ERROR: Activation date cannot be prior to today's date.")
        if expiry < activation_date:
            errors.append("ERROR: Expiration date cannot be prior to activation date.")
        if re_fails(address_pattern, address):
            errors.append("ERROR: Address field is required.")
        if balance < 0:
            errors.append("ERROR: Initial balance cannot be negative.")
        if re_fails(phone_pattern, phone):
            errors.append("ERROR: Phone number must be numeric.")
        if Card.objects.filter(card_number__exact=number).exists():
            errors.append("ERROR: Card number is taken.")

        # Branch if no error recorded
        if not errors:
            account = Account.objects.filter(username__exact=name)[0]
            status = "status" in request.POST
            card = Card(account=account, card_number=int(number), pin=int(pin), date_issued=request.POST['date'],
                        expiry_date=request.POST['expiry'], address=address, active=status)
            card.save()
            return HttpResponseRedirect(reverse('admin_menu', kwargs={'status_code': 4}))

        # Branch if an error was recorded, reload account creation page
        else:
            card_number = randint(0, 999999999)
            card_numbers = [card.card_number for card in Card.objects.all()]
            random_pin = randint(0, 9999)
            users = Account.objects.all()
            # Randomize card_number until a unique one is found.
            while card_number in card_numbers:
                card_number = randint(0, 999999999)
            current_date = timezone.now().date().strftime("%Y-%m-%d")
            expiry_date = (timezone.now() + timedelta(weeks=104)).date().strftime("%Y-%m-%d")
            return render(request, 'atmsite/create_card.html', {'users' :users, 'errors': errors,
                                                                'current_date': current_date, 'expiry':expiry_date,
                                                                'random_pin':random_pin,
                                                                'random_card_number':card_number})

    except ValueError:
        card_number = randint(0, 999999999)
        card_numbers = [card.card_number for card in Card.objects.all()]
        random_pin = randint(0, 9999)
        users = Account.objects.all()
        # Randomize card_number until a unique one is found.
        while card_number in card_numbers:
            card_number = randint(0, 999999999)
        errors.append("ERROR: Balance must be numeric")
        current_date = timezone.now().date().strftime("%Y-%m-%d")
        expiry_date = (timezone.now() + timedelta(weeks=104)).date().strftime("%Y-%m-%d")
        return render(request, 'atmsite/create_card.html', {'users' :users, 'random_pin': random_pin,
                                                            'random_card_number' : card_number, 'errors': errors, 'current_date': current_date, 'expiry_date':expiry_date})


def atm_listing(request):
    atms = ATM.objects.all()
    return render(request, 'atmsite/atm_listing.html', {'atms': atms})


def atm_state(request):
    atm_location = request.GET.get('atm')
    try:
        atm = ATM.objects.filter(current_location__exact=atm_location)[0]
        return render(request, 'atmsite/atm_state.html', {'atm': atm})
    except IndexError:
        return HttpResponseNotFound('<h1>Page not found</h1>')


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


def authenticate_admin(request):
    password = request.POST['password']
    if password == admin_password:
        response = HttpResponseRedirect(reverse('admin_menu'))
        response.set_cookie('admin', True)
        return response
    else:
        return render(request, 'atmsite/index.html', {'error': 'Incorrect password'})


def transfer(request):
    return render(request, 'atmsite/transfer.html')


def transfer_post(request):
    try:
        # Get currently logged in user, or redirect to log in if there is none.
        if request.COOKIES.get('current_account'):
            sending_account = Account.objects.get(id=request.COOKIES.get('current_account'))
        else:
            return HttpResponseRedirect(reverse('index'))
        receiving_username = request.POST['username']
        amount = float(request.POST['amount'])
        receiving_account = Account.objects.filter(username__exact=receiving_username)[0]
        if sending_account.balance > amount:
            sending_account.balance -= amount
            receiving_account.balance += amount
            sending_account.save()
            receiving_account.save()
            return HttpResponseRedirect(reverse('account_menu', kwargs={'status_code': 1}))
        else:
            return render(request, 'atmsite/transfer.html', {'errors': ["Insufficient funds to make transfer"]})
    except IndexError:
        return render(request, 'atmsite/transfer.html', {'errors': ["User does not exist."]})

    except ValueError:
        return render(request, 'atmsite/transfer.html', {'errors': ["Amount field must be a number"]})


def manage_cards(request):
    account_id = request.COOKIES.get('current_account')
    account = Account.objects.get(id=account_id)
    cards = Card.objects.filter(account=account)
    card_numbers = [card.card_number for card in cards]
    card_actives = ["checked" if card.active else "" for card in cards]
    cards = zip(card_numbers, card_actives)
    return render(request, 'atmsite/manage_cards.html', {'cards': cards, 'checked': "checked"})


def manage_cards_post(request):
    account_id = request.COOKIES.get('current_account')
    account = Account.objects.get(id=account_id)
    cards = Card.objects.filter(account=account)
    for card in cards:
        if str(card.card_number) in request.POST.keys():
            card.active = True
        else:
            card.active = False
        card.save()
    return HttpResponseRedirect(reverse('account_menu', kwargs={'status_code': 5}))

