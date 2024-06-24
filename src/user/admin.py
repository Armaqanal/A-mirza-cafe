from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Customer, Staff, User

admin.site.register(Customer)
admin.site.register(Staff)


# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'is_active', 'email', 'is_superuser')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     date_hierarchy = "user__created_at"
#     list_display = ["pk", "balance", "user_photo"]
#
#     def user_photo(self, obj):
#         if obj.user.photo:
#             return format_html('<img src="{}" width="50" />', obj.user.photo.url)
#         return 'N/A'
#
#     user_photo.short_description = 'Photo'
#
#
# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     date_hierarchy = "user__created_at"
#     list_display = ["pk", "user_photo", "edit_record"]
#     list_filter = ["role"]
#     search_fields = ["user__first_name", "user__last_name"]
#     empty_value_display = "N/A"
#
#     def user_photo(self, obj):
#         if obj.user.photo:
#             return format_html('<img src="{}" width="50" />', obj.user.photo.url)
#         return 'N/A'
#
#     user_photo.short_description = 'Photo'
#
#     def edit_record(self, obj):
#         return format_html('<a href="{}">{}</a>', reverse("admin:user_staff_change", args=[obj.pk]),
#                            'edit')
#
#     edit_record.short_description = 'Edit'
