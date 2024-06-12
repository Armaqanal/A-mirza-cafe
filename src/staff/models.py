from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm


class Person(models.Model):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={"unique": "A user with that username already exists."},
    )
    password = models.CharField(max_length=128, validators=[password_validation.validate_password])
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    photo = models.ImageField(
        upload_to='profile_photos/',
        default='profile_photos/default_profile_photo.png',
        blank=True
    )
    phone = models.CharField(max_length=40) # TODO: add a validator
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.password = make_password(self.password)
        super().save()

    def __str__(self):
        return self.username


class Staff(models.Model):
    ROLE_TYPE = [
        ('manager', 'manager'),
        ('barista', 'barista'),
        ('waiter', 'waiter'),
        ('waitress', 'waitress'),
    ]
    salary = models.IntegerField()
    role = models.CharField(max_length=25, choices=ROLE_TYPE, default=ROLE_TYPE[1])
    # todo: change to choice field and check invalid values in the shell
    person_ptr = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name='Person')

    def __str__(self):
        return self.role
