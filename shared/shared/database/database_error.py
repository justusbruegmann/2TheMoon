import httpx
from postgrest import APIError


class DatabaseError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


# Translate postgrest status codes to http error codes.
# See https://docs.postgrest.org/en/stable/references/errors.html for the documentation

_POSTGREST_STATUS_BY_CODE: dict[str, int] = {
        # Group 0 - Connection
        "PGRST000": 503,  # could not connect to the database (bad db-uri or Postgres not running)
        "PGRST001": 503,  # could not connect to the database due to an internal error
        "PGRST002": 503,  # could not connect to the database when building the schema cache
        "PGRST003": 504,  # timed out waiting for a pool connection

        # Group 1 - API Request
        "PGRST100": 400,  # parsing error in the query string parameter
        "PGRST101": 405,  # functions only allow GET and POST
        "PGRST102": 400,  # invalid request body (e.g. empty or malformed JSON)
        "PGRST103": 416,  # invalid range specified for limits/pagination
        "PGRST105": 405,  # invalid PUT request
        "PGRST106": 406,  # schema requested via switching is not in db-schemas
        "PGRST107": 406,  # invalid Accept media type
        "PGRST108": 400,  # filter applied to an embedded resource not present in the select
        "PGRST111": 500,  # invalid response.headers was set
        "PGRST112": 500,  # response.status must be a positive integer
        "PGRST114": 400,  # UPSERT via PUT used together with limit/offset
        "PGRST115": 400,  # UPSERT via PUT with differing primary keys in query string and body
        "PGRST116": 406,  # more than one or no items returned for a singular response
        "PGRST117": 405,  # HTTP verb used is not supported
        "PGRST118": 400,  # tried to order by a related table lacking many-to-one/one-to-one
        "PGRST120": 400,  # embedded resource filtered with an operator other than is.null/not.is.null
        "PGRST121": 500,  # could not parse the JSON objects in a RAISE PGRST error
        "PGRST122": 400,  # invalid preference in the Prefer header with handling=strict
        "PGRST123": 400,  # aggregate functions are disabled
        "PGRST124": 400,  # max-affected preference violated
        "PGRST125": 404,  # invalid path specified in the request URL
        "PGRST126": 404,  # OpenAPI config disabled but the API root path was accessed
        "PGRST127": 400,  # feature specified in the error details is not implemented
        "PGRST128": 400,  # max-affected preference violated by an RPC call
        "PGRST129": 400,  # timezone preference value exceeded 24 characters

        # Group 2 - Schema Cache
        "PGRST200": 400,  # stale foreign key relationship or non-existent embedded resource
        "PGRST201": 300,  # ambiguous embedding request
        "PGRST202": 404,  # stale function signature, or the function does not exist
        "PGRST203": 300,  # overloaded functions requested with the same argument names
        "PGRST204": 400,  # column specified in the columns query parameter was not found
        "PGRST205": 404,  # table specified in the URI was not found

        # Group 3 - JWT
        "PGRST300": 500,  # JWT secret missing from the configuration
        "PGRST301": 401,  # provided JWT couldn't be decoded or is invalid
        "PGRST302": 401,  # request without Bearer auth while the anonymous role is disabled
        "PGRST303": 401,  # JWT claims validation or parsing failed

        # Group X - Internal
        "PGRSTX00": 500,  # internal error in the library used to connect to the database
}


def status_code_of(error: APIError | httpx.HTTPError) -> int | None:
    if isinstance(error, httpx.HTTPStatusError):
        return error.response.status_code
    if isinstance(error, APIError):
        return _POSTGREST_STATUS_BY_CODE.get(error.code or "")
    return None
