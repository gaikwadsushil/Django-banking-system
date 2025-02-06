from django.db import models
from user.models import User
from Account.models import Account
# from Loan.models import Loan
from Transaction.models import Transaction


# from .models import Loan, Transaction

# Create your models here.
STATUS_CHOICE=[
        ('PENDING','PENDING'),
        ('COMPLETED','COMPLETED'),
        ('FAILED','FAILED')
]
METHOD_CHOICE = [
        ('RAZORPAY','RAZORPAY'),
        ('BANK_WALLET','BANK_WALLET')
]

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='payment_user')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_account')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='payment_transaction')
    razorpay_order_id = models.CharField(max_length=25,blank=True,default="default")
    razorpay_payment_id = models.CharField(max_length=25,blank=True,default="default")
    payment_signature=models.CharField(max_length=128,default='default',blank=True)
    amount=models.DecimalField(decimal_places=2,max_digits=12) 
    method = models.CharField(max_length=50, choices=METHOD_CHOICE, default='RAZORPAY')
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='PENDING')
    # timestamp = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f"Payment {self.id} by {self.user.username} "