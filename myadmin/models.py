from django.db import models

# Create your models here.

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catnm=models.CharField(unique=True,max_length=100)
    caticonname=models.CharField(max_length=1000)

class SubCategory(models.Model):
    scatid=models.AutoField(primary_key=True)
    catnm=models.CharField(max_length=100)
    Subcatnm=models.CharField(unique=True,max_length=1000)
    subcaticonname=models.CharField(max_length=1000)  