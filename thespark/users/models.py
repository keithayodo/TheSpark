from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver

# Create your models here.

from allauth.account.signals import user_signed_up

class MyBaseUserManager(BaseUserManager):
	def create_user(self,email,first_name,last_name,occupation,password=None,**extra_fields):
		if not email:
			raise ValueError('users are required to have an email address')

		#research self.model & normalize_email methods
		user = self.model(
			email = MyBaseUserManager.normalize_email(email), #normalize_email lowercases domain part of email
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
		user.is_superuser = True
		user.save(using=self._db)

		return user

#Change model name to AllUser
class AllUser(AbstractBaseUser, PermissionsMixin):
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

	def get_user_type(self):
		return 'all_user'

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name','occupation']


class CounsellorUser(models.Model):
	relation = models.OneToOneField(AllUser,help_text="Connect a Counsellor to a user account.")

	"""
	TODO: Profile picture URL
	"""

	def get_user_type(self):
		return 'counsellor_user'

	def __unicode__(self):
		return self.relation.email

class SparkUser(models.Model):
	relation = models.OneToOneField(AllUser,help_text="Connect a spark user to a user account.")
	bio = models.CharField(max_length=200,null=True,blank=True,help_text="Optional description about this user.")
	fb_link = models.URLField(null=True,blank=True,help_text="Optional link to user's fb profile.")
	twitter_link = models.URLField(null=True,blank=True,help_text="Optional link to user's twitter profile.")

	"""
	TODO: Profile picture URL
	"""

	def get_user_type(self):
		return 'spark_user'

	def __unicode__(self):
		return self.relation.email

ACCEPTED_ACCOMPLISHMENT_CATEGORIES = (
		("Education","Education"),
		("Technology","Technology"),
		("Finance","Finance"),
		("Agriculture","Agriculture"),
	)

class UserAccomplishment(models.Model):
	relation = models.ForeignKey(SparkUser,help_text="Spark user creating the accomplishment.")
	accomplishment_title = models.CharField(max_length=50, help_text="Accomplishment title.")
	accomplishment_summary = models.CharField(max_length=200,help_text="Accomplishment summary.")
	start_date = models.DateField(help_text="Date when this accomplishment began.")
	end_date = models.DateField(help_text="Date when this accomplishment ended.")
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text="Date and Time when this accomplishment was created.")
	updated_at = models.DateTimeField(editable=False,auto_now=True, help_text="Date and time accomplishment last updated.")

	def __unicode__(self):
		return '{0} : {1}'.format(self.relation, self.accomplishment_title)

class UserAccomplishmentTag(models.Model):
	relation = models.ForeignKey(UserAccomplishment,help_text="Accomplishment being tagged.")
	category = models.CharField(max_length=50,choices=ACCEPTED_ACCOMPLISHMENT_CATEGORIES,help_text="Category of tag.")

	class Meta:
		unique_together = ('relation','category')

	def __unicode__(self):
		return '{0} : {1}'.format(self.relation.accomplishment_title,self.category)

@receiver(user_signed_up,dispatch_uid="my.user.sign.up.signal")
def on_user_sign_up(request,user,sociallogin=None,**kwargs):
	if sociallogin:
		if sociallogin.account.provider == 'facebook':
			try:
				new_spark_user = SparkUser.objects.create(relation=user)
				new_spark_user.save()
			except SparkUser.IntegrityError as e:
				return None
