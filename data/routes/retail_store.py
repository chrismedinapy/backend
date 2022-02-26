from django.urls import path

from data.views.retail_store import RetailStoreViewClass

retail_store_routes = [
    path("customers/<str:customer_code>/retail-store/",
         RetailStoreViewClass.as_view({"post", "create"}), name='retail_stores')
]
