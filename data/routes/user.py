from django.urls import path
from data.views import user

user_routes = [
    path('users/signup/', user.UserView.as_view(
        {'post': 'create'}), name='signup'),
]
