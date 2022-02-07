from django.urls import path

from data.views.product_input import ProductInputViewClass


product_input_routes = [

    path("input/products/",
         ProductInputViewClass.as_view({
             "post": "create"}), name="products_input"),
]
