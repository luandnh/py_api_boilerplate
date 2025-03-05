from fastapi import APIRouter, Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
import anyio
import fastapi


from collections.abc import AsyncGenerator, Callable
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import Any

from .config import (
    AppSettings,
    DBSettings,
    RedisSettings,
    EnvironmentOption,
    EnvironmentSettings,
)


async def set_threadpool_tokens(number_of_tokens: int = 100) -> None:
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = number_of_tokens


def lifespan_factory(
    settings: DBSettings | RedisSettings | AppSettings | EnvironmentSettings,
    create_tables_on_start: bool = True,
) -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any]]:
    """Factory to create a lifespan async context manager for a FastAPI app."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        from asyncio import Event

        initialization_complete = Event()
        app.state.initialization_complete = initialization_complete

        await set_threadpool_tokens()

        yield

    return lifespan


def init_app(
    router: APIRouter,
    settings: DBSettings | RedisSettings | EnvironmentSettings,
    migrate_database: bool = True,
    **kwargs,
) -> FastAPI:
    if isinstance(settings, AppSettings):
        app_info = {
            "title": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
        }

        kwargs.update(app_info)

    if isinstance(settings, EnvironmentSettings):
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    lifespan = lifespan_factory(settings, create_tables_on_start=migrate_database)

    application = FastAPI(lifespan=lifespan, **kwargs)
    application.include_router(router)

    if isinstance(settings, EnvironmentSettings):
        docs_router = APIRouter()

        @docs_router.get("/docs", include_in_schema=False)
        async def get_swagger_documentation() -> HTMLResponse:
            html_content = f"""<!doctype html>
            <html>
            <head>
                <title>{kwargs["title"]}</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </head>
            <body>
                <script id="api-reference" data-url="/openapi.json"></script>
                <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
            </body>
            </html>"""

            return HTMLResponse(content=html_content)

        @docs_router.get("/redoc", include_in_schema=False)
        async def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
            return get_redoc_html(openapi_url="/openapi.json", title="docs")

        @docs_router.get("/openapi.json", include_in_schema=False)
        async def openapi() -> dict[str, Any]:
            out: dict = get_openapi(
                title=application.title,
                version=application.version,
                routes=application.routes,
            )
            return out

        application.include_router(docs_router)

    return application
