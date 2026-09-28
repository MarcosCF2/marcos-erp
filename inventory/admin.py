from django.contrib import admin
from .models import StockMovement
from .services import move_stock


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "movement_type", "quantity", "created_by", "created_at")
    list_filter = ("movement_type", "created_at")
    search_fields = ("product__name", "product__sku", "note")
    readonly_fields = ("created_by", "created_at")

    def save_model(self, request, obj, form, change):
        if change:
            return
        movement = move_stock(
            product=obj.product,
            movement_type=obj.movement_type,
            quantity=obj.quantity,
            user=request.user,
            note=obj.note,
        )
        # O admin usa o objeto recebido para registrar o log.
        obj.pk = movement.pk
        obj.created_by = movement.created_by
        obj.created_at = movement.created_at

    def has_change_permission(self, request, obj=None):
        # Movimentação de estoque é histórico: não deve ser editada.
        return obj is None

    def has_delete_permission(self, request, obj=None):
        return False
