from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, phone_number=None, **extra_fields):
        if not (email or phone_number or username):
            raise ValueError('Your email or password or username does not exist')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number, **extra_fields

        )

        user.set_username(username)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True)
    phone_number = models.CharField(verbose_name="phone number", max_length=50, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
