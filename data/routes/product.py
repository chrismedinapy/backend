from django.urls import path

from data.views.product import ProductViewClass


product_routes = [

    path("products/<str:product_code>/",
         ProductViewClass.as_view({"get": "get_product",
                                   "delete":"delete",
                                   "put":"update",
                                   }), name="product"),
    path("products/",
         ProductViewClass.as_view({"get": "get_products",
                                   "post": "create"}), name="products"),
]
