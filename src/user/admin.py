from django.contrib import admin

from .models import Customer, Staff, User

admin.site.register(Customer)
admin.site.register(Staff)




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'is_active', 'email', 'is_superuser')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
