from django.db import models

class Users(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def get_password(self):
        return self.password
    
# Create your models here.
