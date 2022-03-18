import uuid
from datetime import datetime
from django.forms import model_to_dict
from data.models.customer import Customer, CustomerUserGroup
# from data.models.customer_user_group import CustomerUserGroup
from data.models.user import User
from data.utils.constant import AccessLevel, Status
from data.utils.exceptions import EntityNotFound
from data.utils.constant import Status


class CustomerLogic():
    def __init__(self):
        self.fields = ['customer_code',
                       'customer_name', 'customer_description']

    def create(self, customer_data, user_code):
        customer_code = str(uuid.uuid4())
        customer_name = customer_data.get("customer_name")
        customer_description = customer_data.get("customer_description")
        status = Status.ACTIVE.value

        new_customer = Customer(customer_code=customer_code, customer_name=customer_name,
                                customer_description=customer_description, status=status
                                )
        new_customer_saved = Customer.objects.save(new_customer)
        user_login = User.objects.get_user_by_code(user_code)
        customer_user_group = CustomerUserGroup(customer_user_group_code=str(uuid.uuid4()),
                                                customer=new_customer_saved,
                                                status=Status.ACTIVE.value,
                                                user=user_login, user_access_level=AccessLevel.ADMIN.value
                                                )
        customer_user_group_saved = CustomerUserGroup.objects.save(
            customer_user_group)
        return self.__customer_mapped(new_customer_saved)

    def get_customers(self):
        customers = Customer.objects.get_all_customer()
        if not customers:
            raise EntityNotFound(
                f"There are no customers!"
            )
        customer_list = []
        for customer in customers:
            customer_list.append(self.__customer_mapped(customer))
        return customer_list

    def get_customer_by_code(self, customer_code):
        customer = Customer.objects.get_customer_by_code(customer_code)
        if not customer:
            raise EntityNotFound(
                f"There are no customer with code {customer_code}"
            )
        customer_dict = self.__customer_mapped(customer)
        return customer_dict

    def update(self, customer_code, customer_data):
        customer = Customer.objects.get_customer_by_code(customer_code)
        if not customer:
            raise EntityNotFound(
                f"There are no customer with code {customer_code}"
            )
        customer.customer_name = customer_data.get("customer_name")
        customer.customer_description = customer_data.get(
            "customer_description")
        customer_save = Customer.objects.save(customer)
        return self.__customer_mapped(customer_save)

    def delete(self, customer_code):
        customer = Customer.objects.get_customer_by_code(customer_code)
        if not customer:
            raise EntityNotFound(
                f"There is no customer with code {customer_code}"
            )
        customer.status = Status.INACTIVE.value
        Customer.objects.save(customer)

    def __customer_mapped(self, customer):
        customer_dict = model_to_dict(customer, fields=self.fields)
        customer_dict['customer_code'] = str(customer.customer_code)
        return customer_dict
