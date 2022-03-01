from data.logic.customer import CustomerLogic


def seed_customer(customer, user_code):
    customer_logic = CustomerLogic()
    customer = customer_logic.create(customer, user_code)
    customer_code = customer.get("customer_code")

    result = {}
    result["customer_code"] = customer_code

    return result