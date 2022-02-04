from data.logic.login import authenticate


def http_authorization_setup_by_current_user(username, password, client):
    user_credential_data = authenticate(
        {'username': username, 'password': password})
    token = user_credential_data.get('token')
    client.credentials(HTTP_AUTHORIZATION=token)

    return user_credential_data.get('user_code')
