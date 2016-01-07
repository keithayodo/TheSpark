from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class MyAbstractUser(AbstractBaseUser):
	identifier = models.EmailField(unique=True, help_text="User email address.")
	first_name = models.CharField(max_length=50,help_text="User first name.")
	last_name = models.CharField(max_length=50,help_text="User last name.")
	occupation = models.CharField(max_length=50, help_text="User occupation.")
	phone_number = models.CharField(null=True,blank=True,max_length=15,help_text="User mobile number.")
	show_email = models.BooleanField(default=False, help_text="If user allows public email address.")
	show_number = models.BooleanField(default=False, help_text="If user allows public phone number.")

	USERNAME_FIELD = 'identifier'
	REQUIRED_FIELDS = ['first_name','last_name','occupation']
