from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . import models

# admin.site.register(models.Customer)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["id", "username", "photo"]

@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["id", "username", "photo", "edit_record"]
    list_display_links = ["username"]
    list_filter = ["username"]
    search_fields = ["username", "first_name", "last_name"]
    empty_value_field = "N/A"
    # ordering = ["id"]

    def edit_record(self, obj):
        return format_html("<a href={}>{}</a>", reverse("admin:user_staff_change", args=[obj.id]), 'edit')

    edit_record.short_description = 'edit'
    edit_record.admin_order_field = ['id']



