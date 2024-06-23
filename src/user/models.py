import os

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db import models
from pathlib import Path


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(username, email, password, **extra_fields)


class DateFieldsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, PermissionsMixin, DateFieldsMixin):
    def profile_image_upload_to(instance, filename):
        extension = Path(filename).suffix
        return f'profile_photos/{instance.__class__.__name__.lower()}/{instance.username}{extension}'

    # validators
    phone_regex = RegexValidator(
        regex='^(\\+98|0)?9\\d{9}$',
        message='Invalid phone number! Format: +989123456789 or 09123456789'
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=40, validators=[phone_regex])
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(
        upload_to=profile_image_upload_to,
        default='profile_photos/default_profile_photo.png',
        blank=True
    )
    is_confirmEmail = models.BooleanField(default=False)
    enable_two_factor_authentication = models.BooleanField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_confirmEmail = True
            self.enable_two_factor_authentication = False
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"


class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff',
                                primary_key=True)

    # Other fields

    class RoleType(models.TextChoices):
        MANAGER = 'manager', 'manager'
        BARISTA = 'barista', 'barista'
        WAITER = 'waiter', 'waiter'
        WAITRESS = 'waitress', 'waitress'

    salary = models.IntegerField(default=0, blank=False)
    role = models.CharField(max_length=25, choices=RoleType.choices, default=RoleType.BARISTA)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer',
                                primary_key=True)
    balance = models.IntegerField(default=0, blank=False)


@receiver(post_delete, sender=User)
def delete_customer_profile_photo(sender, instance: User, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(pre_save, sender=User)
def delete_old_customer_profile_photo(sender, instance: User, **kwargs):
    if not instance.id:
        return False

    try:
        old_person = User.objects.get(id=instance.id)
    except Customer.DoesNotExist:
        return False

    # TODO: What if my 'upload_to' uses a method that generate file name from username?
    # TODO: What if the user's photo is 'default_profile_?
    if old_person.photo:
        if os.path.isfile(old_person.photo.path):
            os.remove(old_person.photo.path)
