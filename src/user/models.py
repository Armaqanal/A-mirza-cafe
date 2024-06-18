import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from pathlib import Path


class DateFieldsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(DateFieldsMixin, models.Model):
    def profile_image_upload_to(instance, filename):
        extension = Path(filename).suffix
        return f'profile_photos/{instance.__class__.__name__.lower()}/{instance.username}{extension}'

    # validators
    username_validator = UnicodeUsernameValidator()
    phone_regex = RegexValidator(regex='^(\\+98|0)?9\\d{9}$', message='Invalid phone number!')  # TODO: proper message

    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={"unique": "A user with that username already exists."},
    )
    password = models.CharField(max_length=128, validators=[password_validation.validate_password])
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(
        upload_to=profile_image_upload_to,
        default='profile_photos/default_profile_photo.png',
        blank=True
    )
    phone = models.CharField(max_length=40, validators=[phone_regex])
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.password = make_password(self.password)
        super().save()

    def __str__(self):
        return self.username

    class Meta:
        abstract = True


class Staff(Person):
    class RoleType(models.TextChoices):
        MANAGER = 'manager', 'manager'
        BARISTA = 'barista', 'barista'
        WAITER = 'waiter', 'waiter'
        WAITRESS = 'waitress', 'waitress'

    salary = models.IntegerField(default=0, blank=False)
    role = models.CharField(max_length=25, choices=RoleType.choices, default=RoleType.BARISTA)


class Customer(Person):
    balance = models.IntegerField(default=0, blank=False)


@receiver(post_delete, sender=Person)
def delete_customer_profile_photo(sender, instance: Person, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(pre_save, sender=Person)
def delete_old_customer_profile_photo(sender, instance: Person, **kwargs):
    if not instance.id:
        return False

    try:
        old_person = Person.objects.get(id=instance.id)
    except Customer.DoesNotExist:
        return False

    # TODO: What if my 'upload_to' uses a method that generate file name from username?
    # TODO: What if the user's photo is 'default_profile_?
    if old_person.photo:
        if os.path.isfile(old_person.photo.path):
            os.remove(old_person.photo.path)
