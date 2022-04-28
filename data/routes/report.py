from django.urls import path

from data.views.report import ReportViewClass

report_routes = [
    path(
        "customers/<str:customer_code>/reports/",
        ReportViewClass.as_view({"get": "get_all"}),
        name="reports",
    ),
    path(
        "customers/<str:customer_code>/retail-store/<str:retail_store_code>/reports/",
        ReportViewClass.as_view({"get": "get"}),
        name="report",
    ),
]
