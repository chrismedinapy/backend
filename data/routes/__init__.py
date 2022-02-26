from .user import user_routes
from .login import login_routes
from .product import product_routes
from .customer_input import customer_input_routes
from .customer import customer_routes
from .retail_store import retail_store_routes

routes_backoffice = (user_routes + login_routes +
                     product_routes + customer_input_routes + customer_routes + retail_store_routes)
