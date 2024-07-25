from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class mystudent(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)


    
