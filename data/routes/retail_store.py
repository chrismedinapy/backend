from django.urls import path

from data.views.retail_store import RetailStoreViewClass

retail_store_routes = [
    path(
        "customers/<str:customer_code>/retail-store/",
        RetailStoreViewClass.as_view({"post": "create", "get": "get_all"}),
        name="retail_stores",
    ),
    path(
        "customers/<str:customer_code>/retail-store/<str:retail_store_code>/",
        RetailStoreViewClass.as_view({"get": "get"}),
        name="retail-store",
    ),
]
