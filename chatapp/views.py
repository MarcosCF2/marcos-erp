import hashlib
import hmac
import json
import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customers.models import Customer
from .models import Conversation, Message
from .whatsapp import build_automatic_reply, send_whatsapp_text


def _signature_is_valid(request) -> bool:
    app_secret = os.getenv("META_APP_SECRET")
    if not app_secret:
        # Em produção, META_APP_SECRET deve sempre estar configurado.
        return True
    received = request.headers.get("X-Hub-Signature-256", "")
    expected = "sha256=" + hmac.new(
        app_secret.encode("utf-8"), request.body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(received, expected)


def _extract_text_message(payload):
    try:
        value = payload["entry"][0]["changes"][0]["value"]
        message = value["messages"][0]
        if message.get("type") != "text":
            return None
        return {
            "from": message["from"],
            "id": message["id"],
            "text": message["text"]["body"],
        }
    except (KeyError, IndexError, TypeError):
        return None


@csrf_exempt
def webhook(request):
    if request.method == "GET":
        verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
        if request.GET.get("hub.mode") == "subscribe" and request.GET.get("hub.verify_token") == verify_token:
            return HttpResponse(request.GET.get("hub.challenge", ""))
        return HttpResponse("Token inválido", status=403)

    if request.method != "POST":
        return HttpResponse(status=405)

    if not _signature_is_valid(request):
        return HttpResponse("Assinatura inválida", status=403)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)

    incoming = _extract_text_message(payload)
    if not incoming:
        return JsonResponse({"ok": True, "ignored": True})

    # Idempotência: se a Meta repetir o webhook, não respondemos duas vezes.
    if Message.objects.filter(external_id=incoming["id"]).exists():
        return JsonResponse({"ok": True, "duplicate": True})

    customer = Customer.objects.filter(phone=incoming["from"]).first()
    conversation, _ = Conversation.objects.get_or_create(
        whatsapp_phone=incoming["from"],
        defaults={"customer": customer},
    )
    if customer and conversation.customer_id != customer.id:
        conversation.customer = customer
        conversation.save(update_fields=["customer", "updated_at"])

    Message.objects.create(
        conversation=conversation,
        direction=Message.Direction.IN,
        text=incoming["text"],
        external_id=incoming["id"],
    )

    reply = build_automatic_reply(incoming["text"])
    try:
        result = send_whatsapp_text(incoming["from"], reply)
        external_id = result.get("messages", [{}])[0].get("id")
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    Message.objects.create(
        conversation=conversation,
        direction=Message.Direction.OUT,
        text=reply,
        external_id=external_id,
    )
    return JsonResponse({"ok": True})
