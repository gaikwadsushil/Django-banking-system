from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Account
from .forms import AccountForm

# Create your views here.

def Account_list(request):
    Accounts = Account.objects.all()
    return render(request, 'Account/Account_list.html', {'Accounts': Accounts})

def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm()
        return render(request, 'Account/Account_form.html', {'form': form})
    return render(request, 'Account/Account_form.html', {'form': form})

def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'Account/Account_form.html', {'form': form})

def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('account_list')
    return render(request, 'Account/Account_confirm_delete.html', {'account': account})

