# API list contract

The collection endpoints expose one consistent response envelope:

```json
{
  "count": 125,
  "next": "https://api.example.test/api/v1/data/products/?page=2&page_size=20",
  "previous": null,
  "results": []
}
```

## Common query parameters

| Parameter | Behavior |
| --- | --- |
| `page` | One-based page number. Defaults to `1`. |
| `page_size` | Requested number of records. Defaults to `20` and is capped at `100`. |
| `search` | Case-insensitive text search across endpoint-specific public fields. |
| `ordering` | Allowlisted field. Prefix it with `-` for descending order. |

Invalid page values and non-allowlisted ordering fields use the standard API error envelope with `invalid_parameter`.

## Products

`GET /api/v1/data/products/`

- Search: `product_name`, `product_description`
- Ordering: `product_name`, `product_code`
- Default ordering: `product_name`

Example:

```text
/api/v1/data/products/?search=coffee&ordering=-product_name&page=1&page_size=20
```

## Customers

`GET /api/v1/data/customers/`

- Search: `customer_name`, `customer_description`
- Ordering: `customer_name`, `customer_code`
- Default ordering: `customer_name`

## Retail stores

`GET /api/v1/data/customers/{customer_code}/retail-store/`

- Search: `retail_store_name`, `retail_store_city`
- Filter: `retail_store_city`
- Ordering: `retail_store_name`, `retail_store_city`, `retail_store_code`
- Default ordering: `retail_store_name`

Example:

```text
/api/v1/data/customers/{customer_code}/retail-store/?retail_store_city=Limpio&ordering=retail_store_name
```

## Frontend guidance

Clients should use the provided `next` and `previous` URLs rather than rebuilding navigation links. They should treat `count` as the total after filtering and searching, not merely the number of records on the current page.
