from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.link_exceptions import LinkAlreadyExistsError


async def link_already_exists_handler(
    request: Request,
    exc: LinkAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": "This short code is unavailable",
        },
    )
