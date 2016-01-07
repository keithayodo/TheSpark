from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class MyBaseUserManager(BaseUserManager):
	def create_user(self,email,first_name,last_name,occupation,password=None,**extra_fields):
		if not email:
			raise ValueError('users are required to have an email address')

		#research self.model & normalize_email methods
		user = self.model(
			email = MyBaseUserManager.normalize_email(email),
			first_name = first_name,
			last_name = last_name,
			occupation = occupation,
		)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self,email,first_name,last_name,occupation,password,**extra_fields):
		user = self.create_user(email=email,password=password,first_name=first_name,last_name=last_name,occupation=occupation,**extra_fields)
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)

		return user

class MyAbstractUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(unique=True, help_text="User email address.")
	first_name = models.CharField(max_length=50,help_text="User first name.")
	last_name = models.CharField(max_length=50,help_text="User last name.")
	occupation = models.CharField(max_length=50, help_text="User occupation.")
	phone_number = models.CharField(null=True,blank=True,max_length=15,help_text="User mobile number.")
	show_email = models.BooleanField(default=False, help_text="If user allows public email address.")
	show_number = models.BooleanField(default=False, help_text="If user allows public phone number.")
	created_at = models.DateTimeField(editable=False,auto_now_add=True)
	updated_at = models.DateTimeField(editable=False,auto_now=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)


	objects = MyBaseUserManager()

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.first_name

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name','occupation']
