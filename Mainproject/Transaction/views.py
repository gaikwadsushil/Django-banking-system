from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm  
from django.contrib import messages



# Create your views here.
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'Transaction/transaction_list.html', {'transactions': transactions})

def Make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list') 
    else:
        form = TransactionForm()
    return render(request, 'Transaction/Make_transaction.html', {'form': form})

def deposit_money(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'Deposit'
            transaction.sender_account = None  
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'Transaction/deposit_money.html', {'form': form})

def withdraw_money(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'Withdrawal'
            account = form.cleaned_data['sender_account']
            if account.Balance >= form.cleaned_data['amount']:
                transaction.save()
            else:
                form.add_error('amount', 'Insufficient balance')
                return render(request, 'Transaction/withdraw_money.html', {'form': form})
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'Transaction/withdraw_money.html', {'form': form})

def transfer_money(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if transaction.is_balance_sufficient():
                transaction.execute_transaction()
                messages.success(request, 'Money transferred successfully!')
            else:
                messages.error(request, 'Insufficient balance in the sender account.')
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'Transaction/transfer_money.html', {'form': form})