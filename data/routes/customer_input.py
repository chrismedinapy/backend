from django.urls import path

from data.views.customer_input import CustomerInputViewClass


customer_input_routes = [

    path("input/customer/<str:customer_code>/products/",
         CustomerInputViewClass.as_view({
             "post": "create"}), name="products_input"),
]
