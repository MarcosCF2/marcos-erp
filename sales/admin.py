from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ("subtotal",)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_by", "created_at", "total_display")
    list_filter = ("status", "created_at")
    search_fields = ("customer__name", "customer__phone")
    inlines = [SaleItemInline]

    @admin.display(description="Total")
    def total_display(self, obj):
        return obj.total
