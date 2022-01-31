from django.urls import path
from data.views import user_login

user_login_routes = [
    path('signup/', user_login.UserLoginView.as_view(
        {'post': 'create'}), name='signup'),
]
