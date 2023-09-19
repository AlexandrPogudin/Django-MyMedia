from django.db import models

class Users(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
# Create your models here.
