import uuid
# from data.models.customer_user_group import CustomerUserGroup
from data.models.customer import Customer, CustomerUserGroup
from data.models.user import User
from data.utils.constant import AccessLevel, Status
from data.utils.exceptions import EntityNotFound, NotMember


class CustomerUserGroupLogic():
    def __init__(self):
        self.fields = ["customer", "user", "date_join", 'user_access_level']

    def create(self, customer_code, user_code, group_data):
        customer_user_group_code = str(uuid.uuid4())
        if not CustomerUserGroup.objects.check_user_membership(user_code, customer_code):
            raise NotMember(
                f'You are not a member of this customer'
            )
        user = User.objects.get_user_by_code(user_code)
        if not user:
            raise EntityNotFound(
                f"User with code {user_code} not found"
            )
        customer = Customer.objects.get_customer_by_code(customer_code)
        if not customer:
            raise EntityNotFound(
                f"Customer with code: {customer_code} not found"
            )
        username = group_data.get("username")
        member = User.objects.get_user_by_name(username)
        if not member:
            raise EntityNotFound(
                f"User with username: {username} not found"
            )
        new_member = CustomerUserGroup(customer_user_group_code=customer_user_group_code,
                                       customer=customer, user=member, status=Status.ACTIVE.value,
                                       user_access_level=AccessLevel.USER.value)
        CustomerUserGroup.objects.save(new_member)
