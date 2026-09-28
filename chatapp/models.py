from django.db import models
from customers.models import Customer

class Conversation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="conversations")
    whatsapp_phone = models.CharField("WhatsApp", max_length=30, db_index=True)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "conversa"
        verbose_name_plural = "conversas"

    def __str__(self):
        return f"Conversa {self.whatsapp_phone}"


class Message(models.Model):
    class Direction(models.TextChoices):
        IN = "IN", "Recebida"
        OUT = "OUT", "Enviada"

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    direction = models.CharField("direção", max_length=3, choices=Direction.choices)
    text = models.TextField("mensagem")
    external_id = models.CharField("ID WhatsApp", max_length=150, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "mensagem"
        verbose_name_plural = "mensagens"

    def __str__(self):
        return f"{self.get_direction_display()}: {self.text[:40]}"
