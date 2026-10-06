from typing import Annotated

from fastapi import Header, HTTPException


async def check_header_token(token_name: Annotated[str, Header()]):
    # ToDo
    if token_name != "my-secret":
        raise HTTPException(status_code=400, detail="Header token invalid")

