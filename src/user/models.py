import os
from pathlib import Path

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


class DateFieldsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    def profile_image_upload_to(instance, filename):
        extension = Path(filename).suffix
        return f'profile_photos/{instance.__class__.__name__.lower()}/{instance.username}{extension}'

    phone_regex = RegexValidator(regex='^(\\+98|0)?9\\d{9}$', message='Invalid phone number!')  # TODO: proper message

    photo = models.ImageField(
        upload_to=profile_image_upload_to,
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=40, validators=[phone_regex], blank=True)
    address = models.TextField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = []

    # AbstractBaseUser model's __str__ method returns 'username'


class Staff(User):
    class RoleType(models.TextChoices):
        MANAGER = 'manager', 'manager'
        BARISTA = 'barista', 'barista'
        WAITER = 'waiter', 'waiter'
        WAITRESS = 'waitress', 'waitress'

    salary = models.IntegerField(default=0, blank=False)
    role = models.CharField(max_length=25, choices=RoleType.choices, default=RoleType.BARISTA)

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staffs'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.is_staff = True
        super().save()


class Customer(User):
    balance = models.IntegerField(default=0, blank=False)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'


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
