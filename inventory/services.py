from django.core.exceptions import ValidationError
from django.db import transaction

from catalog.models import Product
from .models import StockMovement


@transaction.atomic
def move_stock(
    *,
    product: Product,
    movement_type: str,
    quantity: int,
    user=None,
    note=""
):
    product = Product.objects.select_for_update().get(pk=product.pk)

    if movement_type == StockMovement.MovementType.IN:
        if quantity <= 0:
            raise ValidationError(
                "A quantidade de entrada deve ser maior que zero."
            )

        product.stock += quantity

    elif movement_type == StockMovement.MovementType.OUT:
        if quantity <= 0:
            raise ValidationError(
                "A quantidade de saída deve ser maior que zero."
            )

        if product.stock < quantity:
            raise ValidationError(
                f"Estoque insuficiente. Disponível: {product.stock}."
            )

        product.stock -= quantity

    elif movement_type == StockMovement.MovementType.ADJUST:
        if quantity < 0:
            raise ValidationError(
                "O estoque ajustado não pode ser negativo."
            )

        product.stock = quantity

    else:
        raise ValidationError(
            "Tipo de movimentação inválido."
        )

    product.save(
        update_fields=[
            "stock",
            "updated_at",
        ]
    )

    movement = StockMovement.objects.create(
        product=product,
        movement_type=movement_type,
        quantity=quantity,
        created_by=user,
        note=note,
    )

    return movement