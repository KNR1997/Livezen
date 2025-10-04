"""This module defines the main YMA API endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from livezen.auth.utils import get_current_user
from livezen.auth.views import auth_router
from livezen.auth.views import user_router
from livezen.product.views import router as product_router
from livezen.settings.views import router as settings_router


class ErrorMessage(BaseModel):
    """Represents a single error message."""

    msg: str


class ErrorResponse(BaseModel):
    """Defines the structure for API error responses."""

    detail: list[ErrorMessage] | None = None


api_router = APIRouter(
    prefix="/api/v1",
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

# Public routes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(
    settings_router, prefix="/settings", tags=["Settings"])
api_router.include_router(product_router, prefix="/products", tags=["Product"])

# Private (authenticated) routes
authenticated_api_router = APIRouter(dependencies=[Depends(get_current_user)])
authenticated_api_router.include_router(user_router, prefix="/users", tags=["Users"])
# authenticated_api_router.include_router(product_router, prefix="/products", tags=["Product"])


# Mount the private router into the main one
api_router.include_router(authenticated_api_router)
