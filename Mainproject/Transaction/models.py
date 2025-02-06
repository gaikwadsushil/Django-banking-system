from django.db import models

from Account.models import Account
# from .models import *

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal','Withdrawal'),
        ('transfer', 'Transfer'),
    
    ]
    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions',null=True, blank=True)
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES,  default='Pending')

    date = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)  # For Razorpay integration
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)    

    def __str__(self):
        return f"{self.transaction_type.title()} - {self.amount}"

    def is_balance_sufficient(self):
        """
        Check if the sender account has enough balance for the transaction.
        """
        if self.sender_account and self.amount > self.sender_account.Balance:
            return False
        return True

    def execute_transaction(self):
        """
        Executes the transaction: Updates sender and receiver balances if valid.
        """
        if self.transaction_type == 'transfer' and self.is_balance_sufficient():
            self.sender_account.Balance -= self.amount
            self.receiver_account.Balance += self.amount
            self.sender_account.save()
            self.receiver_account.save()
            self.status = 'success'
        elif self.transaction_type == 'withdrawal' and self.is_balance_sufficient():
            self.sender_account.Balance -= self.amount
            self.sender_account.save()
            self.status = 'success'
        elif self.transaction_type == 'deposit':
            self.receiver_account.Balance += self.amount
            self.receiver_account.save()
            self.status = 'success'
        else:
            self.status = 'failed'
        self.save()