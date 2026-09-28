from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "document",
        "phone",
        "whatsapp",
        "city",
        "state",
        "active",
    )

    list_filter = (
        "active",
        "state",
        "city",
    )

    search_fields = (
        "name",
        "document",
        "phone",
        "whatsapp",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )