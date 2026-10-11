from fastapi import FastAPI

from app.api.exception_handlers import link_already_exists_handler
from app.exceptions.link_exceptions import LinkAlreadyExistsError


def register_exception_handlers(app: FastAPI) -> None:
    handlers = {
        LinkAlreadyExistsError: link_already_exists_handler,
    }

    for exception_class, handler in handlers.items():
        app.add_exception_handler(exception_class, handler)
