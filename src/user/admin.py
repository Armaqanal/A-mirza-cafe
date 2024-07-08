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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_staff', 'is_superuser']
    ordering = ('-date_joined',)
    # fieldsets = (
    #     (None, {'fields': ('email', 'username', 'first_name', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    # )


# admin.site.register(User, AMirzaUserAdmin)


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


admin.site.register(Staff, StaffAdmin)
