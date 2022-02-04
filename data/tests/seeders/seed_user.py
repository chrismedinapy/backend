from data.logic.user import UserLogic
from data.tests.mock.user_login import new_user_mock


def seed_user(user_code,  user):
    user_logic = UserLogic()
    user = user_logic.create(new_user_mock)
    user_code = user.get('user_code')

    result = {}
    result['user_code'] = user_code

    return result