from django.urls import path

from data.views.customer import CustomerViewClass


customer_routes = [
    path(
        "customers/<str:customer_code>/",
        CustomerViewClass.as_view(
            {
                "get": "get_customer",
                "delete": "delete",
                "put": "update",
            }
        ),
        name="customer",
    ),
    path(
        "customers/",
        CustomerViewClass.as_view({"get": "get_customers", "post": "create"}),
        name="customers",
    ),
]
