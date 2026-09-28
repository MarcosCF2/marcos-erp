from django.core.exceptions import ValidationError
from django.db import transaction
from catalog.models import Product
from inventory.models import StockMovement
from inventory.services import move_stock
from .models import Sale, SaleItem

@transaction.atomic
def create_sale(*, customer, items, user=None):
    """items = [{"product_id": 1, "quantity": 2}, ...]"""
    if not items:
        raise ValidationError("A venda precisa ter pelo menos um item.")

    sale = Sale.objects.create(customer=customer, created_by=user)
    for item in items:
        product = Product.objects.select_for_update().get(pk=item["product_id"], active=True)
        quantity = int(item["quantity"])
        move_stock(
            product=product,
            movement_type=StockMovement.MovementType.OUT,
            quantity=quantity,
            user=user,
            note=f"Venda #{sale.pk}",
        )
        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            unit_price=product.price,
        )
    return sale
