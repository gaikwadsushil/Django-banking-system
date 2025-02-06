from datetime import date
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import  AbstractUser
# Create your models here.
GENDER_CHOICES = [
    ("M","Male"),
    ("F","Female"),
    ("O","Other"),
]


class User(AbstractUser):
    contact_detail = models.CharField(max_length=13, default="", null=False, unique=True)
    email = models.EmailField(unique=True, null=False)
    d_o_b = models.DateField(null=False)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default="M")


    def save(self, *args, **kwargs):
        if not self.d_o_b:
            self.d_o_b = date.today()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "User"


class Address(models.Model):
    # contributor = models.ForeignKey(Contributor,on_delete=models.DO_NOTHING)
    address_line_one = models.CharField(max_length=100,default="",null=False)
    address_line_two = models.CharField(max_length=100,default="",null=True)
    street  = models.CharField(max_length=50,default="",null=True)
    area = models.CharField(max_length=50,default="",null=False)
    city = models.CharField(max_length=50,default="",null=False)
    state = models.CharField(max_length=80,default="",null=False)
    country = models.CharField(max_length=50,default="",null=False)

class Documents(models.Model):
    # contributor = models.ForeignKey(Contributor,null=True,on_delete=models.DO_NOTHING)
    address_proof = models.FileField(upload_to='files/documents/address_proof/',default=None,null=True)
    address_proof_verified = models.BooleanField(default=False)
    id_proof = models.FileField(upload_to='files/documents/id_proof/',default=None,null=True)
    id_proof_verified = models.BooleanField(default=False)
