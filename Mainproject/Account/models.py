import uuid
from django.db import models
from user.models import User
from uuid import uuid4

# Create your models here.
# from uuid import uuid4

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    ]
    account_number = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, null=False)
    Balance = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    def __str__(self):
        return f' {self.account_number} - {self.account_type}'