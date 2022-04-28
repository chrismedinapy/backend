from django.urls import path

from data.views.customer_input import CustomerInputViewClass


customer_input_routes = [
    path(
        "customers/<str:customer_code>/retail-store/<str:retail_store_code>/products/",
        CustomerInputViewClass.as_view({"post": "create", "get": "list"}),
        name="products_input",
    ),
]
