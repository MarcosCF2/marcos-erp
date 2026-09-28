from django.conf import settings
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer",
        verbose_name="usuário",
    )

    name = models.CharField(
        "nome / razão social",
        max_length=160,
    )

    document = models.CharField(
        "CPF/CNPJ",
        max_length=18,
        unique=True,
    )

    phone = models.CharField(
        "telefone",
        max_length=20,
        blank=True,
    )

    whatsapp = models.CharField(
        "WhatsApp",
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        "e-mail",
        blank=True,
    )

    cep = models.CharField(
        "CEP",
        max_length=9,
        blank=True,
    )

    address = models.CharField(
        "endereço",
        max_length=180,
        blank=True,
    )

    number = models.CharField(
        "número",
        max_length=20,
        blank=True,
    )

    complement = models.CharField(
        "complemento",
        max_length=100,
        blank=True,
    )

    neighborhood = models.CharField(
        "bairro",
        max_length=100,
        blank=True,
    )

    city = models.CharField(
        "cidade",
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        "estado",
        max_length=2,
        blank=True,
    )

    notes = models.TextField(
        "observações",
        blank=True,
    )

    active = models.BooleanField(
        "ativo",
        default=True,
    )

    created_at = models.DateTimeField(
        "cadastrado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "atualizado em",
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.name