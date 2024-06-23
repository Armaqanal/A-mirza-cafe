from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Customer, Staff

admin.site.register(Customer)
admin.site.register(Staff)

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
