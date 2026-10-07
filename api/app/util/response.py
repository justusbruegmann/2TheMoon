from typing import Any

from fastapi import HTTPException



def success_response(
        data: Any | None = None,
        message: str | None = None
) -> dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data
    }


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
