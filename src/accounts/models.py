import os
from pathlib import Path

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q

from .managers import UserManager


class DateFieldsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    def profile_image_upload_to(instance, filename):
        extension = Path(filename).suffix
        return f"profile_photos/{instance.__class__.__name__.lower()}/{instance.username}{extension}"

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    # Validators
    username_validator = UnicodeUsernameValidator()
    phone_regex = RegexValidator(
        regex="^(\\+98|0)?9\\d{9}$", message="Invalid phone number!"
    )  # TODO: proper message

    # Fields
    # Username Fields:
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        null=True,
        blank=True,
    )
    phone = models.CharField(
        "phone number",
        max_length=40,
        unique=True,
        validators=[phone_regex],
        null=True,
        blank=True,
        default=None,
    )
    email = models.EmailField(
        "Email Address", unique=True, null=True, blank=True, default=None
    )

    # Other Fields:
    photo = models.ImageField(upload_to=profile_image_upload_to, null=True, blank=True)
    date_of_birth = models.DateField("Date Of Birth", null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    address = models.ForeignKey(
        "Address", on_delete=models.SET_NULL, null=True, blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["email", "phone"]

    @property
    def age(self):
        today = timezone.now().date()
        age = int(
            today.year
            - self.date_of_birth.year
            - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
        return age

    def __str__(self):
        return self.username or self.email or self.phone

    def save(self, *args, **kwargs):

        if not (self.username or self.email or self.phone):
            raise ValueError("Providing username, email or phone number is required.")

        if self.email == "":
            self.email = None
        if self.username == "":
            self.username = None
        if self.phone == "":
            self.phone = None

        super().save(*args, **kwargs)

    @property
    def is_customer(self):
        return not self.is_staff


class Address(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    alley = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.city}-{self.state}-{self.neighborhood}-{self.street}"


class Staff(User):
    class RoleType(models.TextChoices):
        MANAGER = "manager", "manager"
        BARISTA = "barista", "barista"
        WAITER = "waiter", "waiter"
        WAITRESS = "waitress", "waitress"

    salary = models.IntegerField(default=0, blank=False)
    role = models.CharField(
        max_length=25, choices=RoleType.choices, default=RoleType.BARISTA
    )

    class Meta:
        verbose_name = "staff"
        verbose_name_plural = "staffs"

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)

        if not self.groups.filter(name='staff').exists():
            if qs := Group.objects.filter(name='staff'):
                staff_group = qs.first()
            else:
                staff_group = Group.objects.create(name='staff')
                order_item = ContentType.objects.get(app_label='order', model='orderitem')
                order = ContentType.objects.get(app_label='order', model='order')
                menu_item = ContentType.objects.get(app_label='menu', model='menuitem')
                menu_category = ContentType.objects.get(app_label='menu', model='menucategory')
                permissions = Permission.objects.filter(
                    Q(content_type=menu_item) |
                    Q(content_type=order) |
                    Q(content_type=order_item) |
                    Q(content_type=menu_category)
                )
                staff_group.permissions.set(permissions)
            self.groups.add(staff_group)
    # def save(self, *args, **kwargs):
    #     self.is_staff = True
    #     if not self.pk:
    #         super().save(*args, **kwargs)
    #
    #         if qs := Group.objects.filter(name='staff'):
    #             staff_group = qs.first()
    #         else:
    #             staff_group = Group.objects.create(name='staff')
    #             order_item = ContentType.objects.get(app_label='order', model='orderitem')
    #             order = ContentType.objects.get(app_label='order', model='order')
    #             menu_item = ContentType.objects.get(app_label='menu', model='menuitem')
    #             menu_category = ContentType.objects.get(app_label='menu', model='menucategory')
    #             permissions = Permission.objects.filter(
    #                 Q(content_type=menu_item) |
    #                 Q(content_type=order) |
    #                 Q(content_type=order_item) |
    #                 Q(content_type=menu_category)
    #             )
    #             staff_group.permissions.set(permissions)
    #         self.groups.add(staff_group)
    #
    #     super().save(*args, **kwargs)


class Customer(User):
    balance = models.IntegerField(default=0, blank=False)

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"


@receiver(post_delete, sender=User)
def delete_customer_profile_photo(sender, instance: User, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

# @receiver(post_save, sender=Staff)  # Replace 'User' with your custom user model if you have one
# def add_staff_group(sender, instance, created, **kwargs):
#     if created and instance.is_staff:
#         if qs := Group.objects.filter(name='staff'):
#             staff_group = qs.first()
#         else:
#             staff_group = Group.objects.create(name='staff')
#             order_item = ContentType.objects.get(app_label='order', model='orderitem')
#             order = ContentType.objects.get(app_label='order', model='order')
#             menu_item = ContentType.objects.get(app_label='menu', model='menuitem')
#             menu_category = ContentType.objects.get(app_label='menu', model='menucategory')
#             permissions = Permission.objects.filter(
#                 Q(content_type=menu_item) |
#                 Q(content_type=order) |
#                 Q(content_type=order_item) |
#                 Q(content_type=menu_category)
#             )
#             staff_group.permissions.set(permissions)
#
#         instance.groups.add(staff_group)
#         instance.save()
