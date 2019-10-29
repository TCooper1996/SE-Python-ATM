from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("bop")


def createAccount(request):
    return HttpResponse("CreateAccount")


def viewAccount(request, account_number):
    return HttpResponse("View account")


def accountMenu(request, account_number):
    return HttpResponse("Control account")

