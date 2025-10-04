import os
import logging

from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from livezen.api import api_router
from livezen.config import TORTOISE_ORM
from livezen.exceptions import BaseAppException
from livezen.logging import configure_logging

PROJECT_ROOT: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))
BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))

print(BASE_DIR)


log = logging.getLogger(__name__)

# we configure the logging level and format
configure_logging()

app = FastAPI()

# Global exception handler


@app.exception_handler(BaseAppException)
async def app_exception_handler(request, exc):
    log.error("Application error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "field": getattr(exc, "field", None)  # for field-specific errors
        }
    )


# Register middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,   # ❌ stop auto-creating tables
    add_exception_handlers=True,
)


app.include_router(api_router)
