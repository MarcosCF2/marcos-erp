import os
import requests
from catalog.models import Product


def send_whatsapp_text(to: str, text: str):
    token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    graph_version = os.getenv("WHATSAPP_GRAPH_VERSION")
    if not token or not phone_number_id or not graph_version:
        raise RuntimeError(
            "Configure WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID e "
            "WHATSAPP_GRAPH_VERSION no .env"
        )

    url = f"https://graph.facebook.com/{graph_version}/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    response = requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def build_automatic_reply(text: str) -> str:
    command = (text or "").strip().lower()
    if command in {"produto", "produtos", "listar produtos", "1"}:
        products = Product.objects.filter(active=True).select_related("category")[:10]
        if not products:
            return "Ainda não há produtos cadastrados."
        lines = ["📦 Produtos disponíveis:"]
        for p in products:
            lines.append(f"• {p.name} — R$ {p.price} — estoque: {p.stock}")
        return "\n".join(lines)

    return (
        "Olá! Eu sou o atendimento Marcos AI.\n"
        "Digite *produtos* ou *1* para listar os produtos disponíveis."
    )
