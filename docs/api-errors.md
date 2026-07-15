# API error contract

All API errors use one JSON envelope:

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "Invalid parameter",
    "fields": {
      "email": ["Enter a valid email address."]
    }
  }
}
```

## Fields

- `error.code` is a stable, machine-readable identifier intended for frontend logic and translations.
- `error.message` is a human-readable summary.
- `error.fields` contains validation messages grouped by request field. It is an empty object for errors that are not tied to specific fields.

Frontend code must branch on `error.code`, not on the English message.

## Standard status codes

| HTTP status | Default code | Meaning |
| --- | --- | --- |
| 400 | `invalid_parameter` | Request validation or parameter failure |
| 401 | `authentication_required` | Authentication is missing or invalid |
| 403 | `permission_denied` | The authenticated caller lacks permission |
| 404 | `not_found` | The requested resource does not exist |
| 409 | `conflict` | The request conflicts with current resource state |
| 415 | `unsupported_media_type` | The submitted content type is unsupported |
| 500 | `internal_error` | An unexpected server error occurred |

Application-specific exceptions may provide a more precise code, such as `invalid_token`, `duplicated_record`, or `not_member`, while retaining the same envelope.

## Security

Unexpected exceptions never expose internal exception messages, database details, stack traces, file paths, or secrets in the HTTP response. Full diagnostic information remains available only in server logs.
