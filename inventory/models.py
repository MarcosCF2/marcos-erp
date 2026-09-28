from django.conf import settings
from django.db import models
from catalog.models import Product

class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "IN", "Entrada"
        OUT = "OUT", "Saída"
        ADJUST = "ADJUST", "Ajuste"

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_movements", verbose_name="produto")
    movement_type = models.CharField("tipo", max_length=10, choices=MovementType.choices)
    quantity = models.PositiveIntegerField("quantidade")
    note = models.CharField("observação", max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "movimentação de estoque"
        verbose_name_plural = "movimentações de estoque"

    def __str__(self):
        return f"{self.product} - {self.get_movement_type_display()} - {self.quantity}"
