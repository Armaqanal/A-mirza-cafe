from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_staff', 'is_superuser']
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    date_hierarchy = "date_joined"
    list_display = ["username", "id", "photo"]

    fields = ['username', 'password', 'first_name', 'last_name', 'email',
              'photo', 'phone', 'address', 'balance', 'is_active']


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    date_hierarchy = "date_joined"

    fields = ['username', 'password', 'first_name', 'last_name', 'email',
              'photo', 'phone', 'address', 'salary', 'role', 'is_active']
    readonly_fields = ['is_active']
