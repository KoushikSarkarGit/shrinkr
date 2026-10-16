from fastapi import FastAPI

from app.api.exception_handlers import link_already_exists_handler, link_not_found_handler
from app.exceptions.link_exceptions import LinkAlreadyExistsError, LinkNotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    handlers = {
        LinkAlreadyExistsError: link_already_exists_handler,
        LinkNotFoundError: link_not_found_handler,
    }

    for exception_class, handler in handlers.items():
        app.add_exception_handler(exception_class, handler)
