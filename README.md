# Marcos ERP + WhatsApp — MVP didático

Projeto em **Python + Django 5.2 LTS** para construir, na ordem correta:

- Admin: categorias, produtos, estoque, clientes, usuários, vendas e chat.
- Cliente: listagem de produtos e histórico de compras.
- WhatsApp: webhook, histórico de conversa e comando para listar produtos.

> O projeto usa SQLite no desenvolvimento para você começar sem instalar banco externo. Quando estiver estável, migraremos para PostgreSQL sem mudar os models.

## 1. Abrir no VS Code

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env`.

## 2. Criar o banco

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 3. Rodar

```bash
python manage.py runserver
```

Abra:
- `http://127.0.0.1:8000/admin/`
- `http://127.0.0.1:8000/produtos/`
- `http://127.0.0.1:8000/historico/`

## Ordem de estudo dos arquivos

1. `config/settings.py`
2. `catalog/models.py` → `catalog/admin.py`
3. `inventory/models.py` → `inventory/services.py`
4. `customers/models.py` → `customers/admin.py`
5. `sales/models.py` → `sales/services.py` → `sales/admin.py`
6. `portal/views.py` → `portal/urls.py` → templates
7. `chatapp/models.py`
8. `chatapp/whatsapp.py`
9. `chatapp/views.py` → `chatapp/urls.py`
10. `.env` e configuração do webhook na Meta
11. Git/GitHub

## Observação sobre venda e estoque

O `create_sale()` em `sales/services.py` é o caminho correto para criar vendas programaticamente porque desconta estoque de forma transacional. Movimentações de estoque criadas pelo Admin passam pelo mesmo serviço e ficam imutáveis como histórico. Na próxima evolução criaremos uma tela/formulário próprio de venda no painel para garantir que toda venda feita pela interface também use o serviço transacional.
