from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("direction", "text", "external_id", "created_at")

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("whatsapp_phone", "customer", "updated_at")
    search_fields = ("whatsapp_phone", "customer__name")
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "direction", "short_text", "created_at")
    list_filter = ("direction", "created_at")

    @admin.display(description="Mensagem")
    def short_text(self, obj):
        return obj.text[:70]
