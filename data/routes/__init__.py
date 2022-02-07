from .user import user_routes
from .login import login_routes
from .product import product_routes
from .product_input import product_input_routes

routes_backoffice = (user_routes + login_routes +
                     product_routes + product_input_routes)
