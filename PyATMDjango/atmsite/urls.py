from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name="index"),
        path('<int:status_code>/', views.index, name="index"),
        path('accountmenu/', views.account_menu, name='account_menu'),
        path('accountmenu/<int:status_code>/', views.account_menu, name='account_menu'),
        path('authenticateaccount', views.authenticate_account, name='authenticate_account'),
        path('createaccountpost', views.create_account_post, name='create_account_post'),
        path('createaccount', views.create_account, name='create_account'),
        path('withdraw/', views.withdraw, name='withdraw'),
        path('withdrawpost/', views.withdraw_post, name='withdraw_post'),
        path('deposit/', views.deposit, name='deposit'),
        path('depositpost/', views.deposit_post, name='deposit_post'),
        path('viewbalance/', views.view_balance, name='view_balance'),
        ]
