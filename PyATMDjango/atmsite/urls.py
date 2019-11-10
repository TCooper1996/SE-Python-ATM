from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name="index"),
        path('adminlogin/', views.admin_login, name="admin_login"),
        path('<int:status_code>/', views.index, name="index"),
        path('accountmenu/', views.account_menu, name='account_menu'),
        path('accountmenu/<int:status_code>/', views.account_menu, name='account_menu'),
        path('adminmenu/', views.admin_menu, name='admin_menu'),
        path('adminmenu/<int:status_code>/', views.admin_menu, name='admin_menu'),
        path('authenticateaccount', views.authenticate_account, name='authenticate_account'),
        path('authenticateadmin', views.authenticate_admin, name='authenticate_admin'),
        path('createaccountpost', views.create_account_post, name='create_account_post'),
        path('createaccount', views.create_account, name='create_account'),
        path('createcard', views.create_card, name='create_card'),
        path('createcardpost', views.create_card_post, name='create_card_post'),
        path('atmlisting', views.atm_listing, name='atm_listing'),
        path('atmstate', views.atm_state, name='atm_state'),
        path('withdraw/', views.withdraw, name='withdraw'),
        path('withdrawpost/', views.withdraw_post, name='withdraw_post'),
        path('deposit/', views.deposit, name='deposit'),
        path('depositpost/', views.deposit_post, name='deposit_post'),
        path('viewbalance/', views.view_balance, name='view_balance'),
        path('transfer/', views.transfer, name='transfer'),
        path('transferpost/', views.transfer_post, name='transfer_post'),

]
