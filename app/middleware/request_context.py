import time

from fastapi import Request


async def request_context_middleware(req: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(req)

    duration = time.perf_counter() - start_time

    response.headers["performance"] = f"{duration:.6f}s"

    return response
