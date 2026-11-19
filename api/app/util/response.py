from functools import wraps
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

from shared.database import DatabaseError


############################
# This error is raised by domain functions to signalize failures in business-logic
# It hands a HTTP status code through to be passed in a HTTP error response
############################
class DomainError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


############################
# A wrapper to send a 2XX HTTP response
############################
def success_response(
        data: Any | None = None,
        message: str | None = None
) -> dict[str, Any]:
    return {
            "success": True,
            "message": message,
            "data": data
    }


############################
# A wrapper to send a 4XX/5XX HTTP error response
############################
def error_response(
        status_code: int,
        data: Any | None = None,
        message: str | None = None
) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
                "success": False,
                "message": message,
                "data": data
        }
    )


############################
# A thin wrapper to send an error response from a given DatabaseError
############################
def db_error_response(e: DatabaseError) -> HTTPException:
    return error_response(status_code=e.status_code or 503, message=str(e))



def _unwrap(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=True, mode="json")
    if isinstance(value, list):
        return [_unwrap(v) for v in value]
    return value


def api_response(func):
    ############################
    # A decorator to cut down big amounts of boilerplate that differentiates between a success or error response.
    # It is to be used in the routers (not in the domain functions, because API responses are HTTP concerns and thus
    # part of the router and explicitly not the domain). Look in any router on how to decorate the handler functions.
    ############################

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # The domain logic function is called here
            result = func(*args, **kwargs)
        except DatabaseError as e:
            raise db_error_response(e)
        except DomainError as e:
            raise error_response(status_code=e.status_code, message=e.message)
        return success_response(data=_unwrap(result))

    return wrapper
