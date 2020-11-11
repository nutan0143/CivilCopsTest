from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class BaseModel(models.Model):
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)

	class Meta:
		abstract=True

class MyUserManager(BaseUserManager):
	"""Base User class for creating Superuser"""
	def create_superuser(self, email_address, password):
		user = self.model(email_address=email_address)
		user.set_password(password)
		user.is_superuser = True
		user.is_active = True
		user.is_staff = False
		user.save(using=self._db)
		return user

	def create_user(self, email_address, password=None, username=''):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email_address:
		    raise ValueError('Users must have an Email Address')

		user = self.model(
		    email_address=self.email_address,
		    is_active=False,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

class User(AbstractBaseUser,BaseModel):
	"""User Information table"""
	full_name = models.CharField(
		"Full Name", max_length=100
	)
	email_address = models.EmailField(
		"Email Address", unique=True, max_length=50
	)
	is_superuser = models.BooleanField(
		"Super User", default=False
	)
	is_staff = models.BooleanField(
		"Staff", default=False
	)
	is_active = models.BooleanField(
		"Status", default=False
	)

	objects = MyUserManager()
	USERNAME_FIELD = 'email_address'

	def has_module_perms(self, app_label):
		return self.is_superuser

	def __str__(self):
		return self.email_address

class UserInterest(BaseModel):
	"""User Interest table"""
	user = models.ForeignKey(
		User, on_delete=models.CASCADE, related_name='user_intertest'
	)
	interest = models.CharField(
		"User Interest", max_length=50
	)

	def __str__(self):
		return "{} intertest is {}".format(self.user.full_name,self.intertest)
