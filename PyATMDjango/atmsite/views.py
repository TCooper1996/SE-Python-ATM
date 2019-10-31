from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import randint

from .models import Account, Card


# Create your views here.
def index(request):
    return render(request, "atmsite/index.html")


def create_account(request):
    return render(request, 'atmsite/create_account.html')


def view_balance(request, account_hash):
    return HttpResponse("View account balance")


def account_menu(request, account_hash):
    pass
    #return render(request, 'atmsite/account_menu.html')


def create_account_post(request):
    try:
        name = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        account = Account(username=name, password=password, phone_number=phone, address=address)
        account.account_number = randint(0, 10000)
        if account.tryhash():
            account.save()
            #return HttpResponseRedirect(reverse('account_menu') + account.account_hash)
        else:
            # TODO: Handle this branch
            pass

    except KeyError:
        pass
        #return render(request, 'atmsite/create_account.html', {'error': "All fields are required"})


def authenticate_account(request):
    try:
        name = request.POST['username']
        password = request.POST['password']
        a = Account.objects.filter(username__exact=name)[0]
        if a.password == password:
            print("asdasd")
            #HttpResponseRedirect(reverse('account_menu', kwargs={'account_hash': a.account_hash}))
        else:
            return render(request, 'atmsite/index.html', {'error': 'Unknown or Incorrect username/password'})

    except IndexError:
        return render(request, 'atmsite/index.html', {'error': 'Unknown or Incorrect username/password'})