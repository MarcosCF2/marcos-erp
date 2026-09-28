from django.urls import path
from . import views

app_name = "portal"
urlpatterns = [
    path("", views.home, name="home"),
    path("produtos/", views.product_list, name="product-list"),
    path("historico/", views.sale_history, name="sale-history"),
]
