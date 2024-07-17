from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .forms import (
    CustomerChangeForm,
    CustomerCreationForm,
    StaffChangeForm,
    StaffCreationForm
)
from .models import User, Customer, Staff
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.contrib.contenttypes.models import ContentType


class AMirzaUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', 'email', 'phone', 'is_staff', 'is_superuser']
    list_filter = ['username', 'email', 'phone', ]
    readonly_fields = ['last_login', 'date_joined', 'date_modified']
    fieldsets = [
        (None, {
            "fields": (
                "username", "email", "phone", "password")
        }),
        ('Personal Info', {
            "fields": ["first_name", "last_name", "address", "gender", "date_of_birth", "photo", "date_joined",
                       "date_modified",
                       "last_login"
                       ]
        }),
        ("Permissions", {
            "fields":
                ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
        }),
    ]
    add_fieldsets = [
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "password1", "password2")
        }),
        ('Personal Info', {
            "fields": ["first_name", "last_name", "address", "gender", "date_of_birth", "photo", "date_joined",
                       "date_modified",
                       "last_login"
                       ]
        }),
        ("Permissions",
         {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
          }),
    ]
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, AMirzaUserAdmin)


class CustomerAdmin(AMirzaUserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    fieldsets = (
        (None, {
            "fields": (
                "username", "email", "phone", "password")
        }),
        ('Personal Info', {
            "fields": ("first_name", "last_name", "address", "gender", "date_of_birth", "photo", "date_joined",
                       "date_modified",
                       "last_login")
        }),
        ('Customer Fields', {
            'fields': ('balance',)
        }),
        ("Permissions", {
            "fields":
                ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "password1", "password2")
        }),
        ('Personal Info', {
            "fields": ("first_name", "last_name", "address", "gender", "date_of_birth", "photo", "date_joined",
                       "date_modified",
                       "last_login")
        }),
        ('Customer Fields', {
            'fields': ('balance',)
        }),

        ("Permissions",
         {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
          }),
    )


admin.site.register(Customer, CustomerAdmin)


class StaffAdmin(AMirzaUserAdmin):
    add_form = StaffCreationForm
    form = StaffChangeForm
    fieldsets = (
        (None, {
            "fields": (
                "username", "email", "phone", "password")
        }),
        ('Personal Info', {
            "fields": ("first_name", "last_name", "address", "gender", "date_of_birth", "photo", "date_joined",
                       "date_modified",
                       "last_login")
        }),
        ('Customer Fields', {
            'fields': ('salary', 'role')
        }),
        ("Permissions", {
            "fields":
                ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "password1", "password2")
        }),
        ('Personal Info', {
            "fields": ("first_name", "last_name", "address", "gender", "date_of_birth", "photo", "date_joined",
                       "date_modified",
                       "last_login")
        }),
        ('Staff Fields', {
            'fields': ('salary', 'role')
        }),

        ("Permissions",
         {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
          }),
    )

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     if qs := Group.objects.filter(name='staff'):
    #         staff_group = qs.first()
    #     else:
    #         staff_group = Group.objects.create(name='staff')
    #         order_item = ContentType.objects.get(app_label='order', model='orderitem')
    #         order = ContentType.objects.get(app_label='order', model='order')
    #         menu_item = ContentType.objects.get(app_label='menu', model='menuitem')
    #         menu_category = ContentType.objects.get(app_label='menu', model='menucategory')
    #         permissions = Permission.objects.filter(
    #             Q(content_type=menu_item) |
    #             Q(content_type=order) |
    #             Q(content_type=order_item) |
    #             Q(content_type=menu_category)
    #         )
    #         staff_group.permissions.set(permissions)
    #     obj.groups.add(staff_group)
    #     obj.save()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.groups.filter(name='staff').exists():
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
            obj.groups.add(staff_group)
        obj.save()


admin.site.register(Staff, StaffAdmin)
