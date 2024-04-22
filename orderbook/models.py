from django.db import models

# Create your models here.
class Cart(models.Model):
    bookCode=models.CharField(max_length=200)
    customerCode=models.CharField(max_length=200)
    quantity=models.IntegerField(null=True)

class Order(models.Model):
    bookCode=models.CharField(max_length=200)
    customerCode=models.CharField(max_length=200)
    quantity=models.IntegerField(null=True,default=0)
    price=models.FloatField(null=True,default=0.0)
    total=models.FloatField(null=True,default=0.0)
    dateOrd=models.DateField(null=True)
    status=models.IntegerField(null=True,default=0)


