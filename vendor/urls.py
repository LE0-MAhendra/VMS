from django.urls import path, include
from . import views

urlpatterns = [
    # vendor urls
    path("vendors/", views.vendors, name="all_vendors"),
    path("vendors/<int:pk>/", views.vendor, name="vendor"),
    # Purchase_order urls
    path("purchase_orders/", views.purchase_orders, name="POs"),
    path("purchase_orders/<int:pk>/", views.purchase_order, name="Edit_PO"),
    # Vendor Performance urls
    path("vendors/<int:pk>/performance", views.get_performance, name="performance"),
]
