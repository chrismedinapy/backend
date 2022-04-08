from .user import user_routes
from .login import login_routes
from .product import product_routes
from .customer_input import customer_input_routes
from .customer import customer_routes
from .retail_store import retail_store_routes
from .customer_user_group import customer_user_group_routes
from .report import report_routes 
routes_backoffice = (user_routes + login_routes +
                     product_routes + customer_input_routes +
                     customer_routes + retail_store_routes +
                     customer_user_group_routes + report_routes)
