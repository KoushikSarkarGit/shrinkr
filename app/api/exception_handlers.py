from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.link_exceptions import LinkAlreadyExistsError, LinkNotFoundError


async def link_already_exists_handler(
    request: Request, exc: LinkAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=409, content={"detail": "This short code is unavailable"}
    )


async def link_not_found_handler(
    request: Request, exc: LinkNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404, content={"detail": f"Link not found for code: {exc.code}"}
    )
