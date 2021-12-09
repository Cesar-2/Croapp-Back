from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Auth(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    is_disabled = models.BooleanField(default=False)
    token = models.TextField("Token", max_length=700)

    class Meta:
        verbose_name = "Sessin"
        verbose_name_plural = "Sessions"

    def __str__(self):
        return self.token


class Profile(models.Model):
    names = models.CharField("Profile names", max_length=255)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.names


class User(AbstractUser):
    phone_number = models.CharField('Phone number', max_length=15)
    citizen_code = models.CharField('Citizen code', max_length=11)
    email = models.EmailField('Email address', max_length=255, unique=True)
    amount_expense = models.IntegerField("Expense", default=0)
    profile = models.ManyToManyField(
        Profile, blank=True, related_name='user_profile')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
