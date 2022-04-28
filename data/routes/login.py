from django.urls import path

from data.views import login


login_routes = [
    path(
        "users/login/",
        login.LoginViewSet.as_view({"post": "authenticate"}),
        name="authentication",
    ),
    path(
        "users/login/refresh/",
        login.LoginViewSet.as_view({"post": "refresh_token"}),
        name="refresh",
    ),
]
