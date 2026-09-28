from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from catalog.models import Product
from sales.models import Sale


def home(request):
    return render(request, "portal/home.html")


def product_list(request):
    products = Product.objects.filter(active=True).select_related("category")
    return render(request, "portal/product_list.html", {"products": products})


@login_required
def sale_history(request):
    try:
        customer = request.user.customer_profile
    except Exception:
        sales = Sale.objects.none()
    else:
        sales = Sale.objects.filter(customer=customer).prefetch_related("items__product")
    return render(request, "portal/sale_history.html", {"sales": sales})
