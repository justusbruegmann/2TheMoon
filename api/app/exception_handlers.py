from typing import Any

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse



async def exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body: dict[str, Any] = {"success": False}

    detail: Any = exc.detail # This is just for typing to remove an IDE warning
    if isinstance(detail, dict):
        body.update(detail)
    else:
        body["message"] = detail

    return JSONResponse(status_code=exc.status_code, content=body)
