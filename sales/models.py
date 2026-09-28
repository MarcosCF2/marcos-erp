from decimal import Decimal
from django.conf import settings
from django.db import models
from customers.models import Customer
from catalog.models import Product

class Sale(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Aberta"
        PAID = "PAID", "Paga"
        CANCELED = "CANCELED", "Cancelada"

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="sales", verbose_name="cliente")
    status = models.CharField("status", max_length=12, choices=Status.choices, default=Status.OPEN)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "venda"
        verbose_name_plural = "vendas"

    @property
    def total(self):
        return sum((item.subtotal for item in self.items.all()), Decimal("0.00"))

    def __str__(self):
        return f"Venda #{self.pk} - {self.customer}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("quantidade")
    unit_price = models.DecimalField("preço unitário", max_digits=12, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product} x {self.quantity}"
