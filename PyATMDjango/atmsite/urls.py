from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name="index"),
        path('accountmenu/<int:account_number>', views.accountMenu, name='accountMenu'),
        path('createaccount', views.createAccount, name='createAccount'),
        path('viewaccount/<int:account_number>', views.viewAccount, name='viewAccount'),
        ]
