import asyncio
import logging
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.category import router as category_router
from src.api.routers.task import router as task_router
from src.core.config import settings
from src.core.logging import configure_logging

configure_logging()

app = FastAPI()
# TODISCUSS
app.state.request_count = 0
app.state.request_count_lock = asyncio.Lock()
logger = logging.getLogger("app.middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)
    except:
        duration_ms = (perf_counter() - started_at) * 1_000
        logger.exception(
            "Request failed: %s %s completed in %.2f ms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1_000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.middleware("http")
async def count_requests(request: Request, call_next) -> Response:
    response: Response = await call_next(request)

    async with app.state.request_count_lock:
        app.state.request_count += 1
        request_number = app.state.request_count

    response.headers["X-Request-number"] = str(request_number)
    return response


app.include_router(router=task_router)
app.include_router(router=category_router)
