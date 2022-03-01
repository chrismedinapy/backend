from django.urls import path

from data.views.customer_user_group import CustomerUserGroupClassView

customer_user_group_routes = [

    path('customers/<str:customer_code>/group/',
    CustomerUserGroupClassView.as_view({
        "post":"create"
    }), name = "group")
]