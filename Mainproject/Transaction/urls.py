from django.urls import path
from . import views

urlpatterns = [
    path('Transaction/', views.transaction_list, name='transaction_list'), 
    path('Make_transaction/', views.Make_transaction, name='Make_transaction'),
    path('deposit_money.html/', views.deposit_money, name='deposit_money'),
    path('withdraw_money.html/', views.withdraw_money, name='withdraw_money'),
    path('transfer_money.html/',views.transfer_money,name='transfer_money'),


]