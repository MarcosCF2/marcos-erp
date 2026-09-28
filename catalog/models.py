from django.db import models

class Category(models.Model):
    name = models.CharField("nome", max_length=120, unique=True)
    active = models.BooleanField("ativa", default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="categoria")
    name = models.CharField("nome", max_length=160)
    sku = models.CharField("SKU", max_length=60, unique=True)
    description = models.TextField("descrição", blank=True)
    price = models.DecimalField("preço", max_digits=12, decimal_places=2)
    stock = models.IntegerField("estoque atual", default=0)
    active = models.BooleanField("ativo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    def __str__(self):
        return f"{self.name} ({self.sku})"
