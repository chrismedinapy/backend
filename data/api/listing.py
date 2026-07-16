"""Reusable pagination, filtering, search, and ordering for API list responses."""

from urllib.parse import urlencode

from data.utils.exceptions import InvalidParameter

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def _positive_int(value, name, default):
    if value in (None, ""):
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise InvalidParameter(f"{name} must be a positive integer") from exc
    if parsed < 1:
        raise InvalidParameter(f"{name} must be a positive integer")
    return parsed


def _page_url(request, page):
    params = request.query_params.copy()
    params["page"] = page
    query = urlencode(params, doseq=True)
    return request.build_absolute_uri(f"{request.path}?{query}")


def paginate_list(
    request,
    items,
    *,
    search_fields=(),
    ordering_fields=(),
    filter_fields=(),
    default_ordering=None,
):
    """Apply allowlisted query operations and return a stable page envelope."""

    result = list(items)

    for field in filter_fields:
        value = request.query_params.get(field)
        if value not in (None, ""):
            result = [item for item in result if str(item.get(field, "")) == value]

    search = request.query_params.get("search", "").strip().casefold()
    if search:
        result = [
            item
            for item in result
            if any(search in str(item.get(field, "")).casefold() for field in search_fields)
        ]

    ordering = request.query_params.get("ordering") or default_ordering
    if ordering:
        descending = ordering.startswith("-")
        field = ordering[1:] if descending else ordering
        if field not in ordering_fields:
            raise InvalidParameter(f"ordering must be one of: {', '.join(ordering_fields)}")
        result.sort(
            key=lambda item: (item.get(field) is None, str(item.get(field, "")).casefold()),
            reverse=descending,
        )

    page = _positive_int(request.query_params.get("page"), "page", 1)
    requested_page_size = _positive_int(
        request.query_params.get("page_size"), "page_size", DEFAULT_PAGE_SIZE
    )
    page_size = min(requested_page_size, MAX_PAGE_SIZE)
    count = len(result)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "count": count,
        "next": _page_url(request, page + 1) if end < count else None,
        "previous": _page_url(request, page - 1) if page > 1 and start < count else None,
        "results": result[start:end],
    }
