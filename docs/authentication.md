# Authentication contract

## Login

`POST /api/v1/data/users/login/`

Request:

```json
{"username": "user@example", "password": "secret"}
```

Response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "user_code": "...",
    "name": "...",
    "access_level": 1
  }
}
```

## Authenticated requests

Send exactly one HTTP authorization header:

```http
Authorization: Bearer <access_token>
```

The API rejects missing headers, other schemes, empty tokens, malformed headers, refresh tokens used as access tokens, missing claims, expired tokens, invalid signatures, and tokens whose user no longer exists.

## Refresh

`POST /api/v1/data/users/login/refresh/`

Request:

```json
{"refresh_token": "..."}
```

A successful refresh returns the same response contract as login and rotates both tokens. Access tokens cannot be used at the refresh endpoint.

## Lifetime configuration

- `ACCESS_TOKEN_EXPIRE_SECONDS`, default `86400`
- `REFRESH_TOKEN_EXPIRE_DAYS`, default `7`

Frontend code should use `expires_in` rather than duplicating backend lifetime configuration.

## Cache isolation

Authenticated cached endpoints vary by the `Authorization` header. They must not vary only by cookies because JWT identity is transported in the Bearer token.
