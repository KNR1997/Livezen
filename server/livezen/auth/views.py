from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from tortoise.expressions import Q

from livezen.auth.permissions import AdminPermission, PermissionsDependency
from livezen.auth.utils import CurrentUser, create_access_token
from livezen.config import YMA_JWT_EXP
from livezen.exceptions import ConflictException, ResourceNotFoundException

from .models import AdminPasswordReset, ChangePasswordUserInput, JWTOut, JWTPayload, UpdateEmailUserInput, UserCreate, UserLogin, UserPagination, UserRead, UserReadSimple, UserRegister, UserUpdate
from livezen.enums import UserRole

from .repository import UserRepository
from .services.user_service import UserService
from .services.auth_service import AuthService


auth_router = APIRouter()
user_router = APIRouter()

user_service = UserService(UserRepository())
auth_service = AuthService(UserRepository())


@auth_router.post("/register", response_model=JWTOut)
async def register_user(user_in: UserRegister):
    existing_user = await user_service.get_by_email(email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "msg": "A user with this email already exists.",
                "loc": ["email"],
                "type": "value_error",
            }],
        )
    user = await auth_service.register(user_in=user_in)
    role: UserRole = user.role
    access_token_expires = timedelta(minutes=YMA_JWT_EXP)
    expire = datetime.now(timezone.utc) + access_token_expires
    return JWTOut(
        token=create_access_token(
            data=JWTPayload(
                user_id=str(user.id),
                email=user.email,
                exp=expire,
            )
        ),
        email=user.email,
        username=user.username,
        role=role,
        permissions=[role]
    )


@auth_router.post("/token", summary="Get token", response_model=JWTOut)
async def login_access_token(credentials: UserLogin):
    user = await auth_service.authenticate(credentials)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    role: UserRole = user.role

    # await user_service.update_last_login(user.id)
    access_token_expires = timedelta(minutes=YMA_JWT_EXP)
    expire = datetime.now(timezone.utc) + access_token_expires

    return JWTOut(
        token=create_access_token(
            data=JWTPayload(
                user_id=str(user.id),
                email=user.email,
                exp=expire,
            )
        ),
        email=user.email,
        username=user.username,
        role=role,
        permissions=[role]
    )


@auth_router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}


@auth_router.get("/me", response_model=UserRead)
def get_me(*, current_user: CurrentUser):
    return current_user


# Mapping of special search keys → list of model fields to search
SEARCH_FIELD_MAPPINGS = {
    "name": ["first_name", "last_name", "email", "username"],
}


@user_router.get("", response_model=UserPagination)
async def paginated_users(
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
    search: Optional[str] = Query(""),
    searchJoin: str = Query(
        "and", description="'and' or 'or' join for multiple search conditions"),
    role: Optional[str] = None,
):
    q = Q()
    if search:
        # Example: search="name:english;status:active"
        filters = search.split(";")
        for f in filters:
            try:
                field, value = f.split(":", 1)

                if field in SEARCH_FIELD_MAPPINGS:
                    # Build OR condition for all mapped fields
                    condition = Q()
                    for mapped_field in SEARCH_FIELD_MAPPINGS[field]:
                        condition |= Q(**{f"{mapped_field}__icontains": value})
                else:
                    # Normal single-field search
                    lookup = {f"{field}__icontains": value}
                    condition = Q(**lookup)

                if searchJoin.lower() == "or":
                    q |= condition
                else:
                    q &= condition
            except ValueError:
                continue  # skip invalid filter format
    if role:
        q = Q(role=role)

    total, data = await user_service.paginated(page=page, page_size=page_size, search=q)
    return UserPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        perPage=page_size,
        total=total,
    )


@user_router.post(
    "",
    response_model=UserRead,
)
async def create_user(
    user_in: UserCreate,
    current_user: CurrentUser,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
):
    """Creates a new user."""
    if await user_service.get_by_email(email=user_in.email):
        raise ConflictException(
            "User with this email already exists", field="email")

    user = await user_service.create(user_in=user_in)
    return user


@user_router.put(
    "/{user_id}",
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
    response_model=UserRead,
)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: CurrentUser,
):
    """Update a user."""
    user = await user_service.get(user_id=user_id)
    if not user:
        raise ResourceNotFoundException(
            "A subject with this id does not exist.")
    return await user_service.update(user=user, user_in=user_in)


@user_router.post("/{user_id}/reset-password", response_model=UserRead)
def admin_reset_password(
    user_id: int,
    password_reset: AdminPasswordReset,
    current_user: CurrentUser,
):
    # """Admin endpoint to reset user password"""
    # # Verify current user is an admin
    # if not current_user.is_admin():
    #     print('not a admin')
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=[{"msg": "Only admins can reset passwords"}],
    #     )

    # user = get(db_session=db_session, user_id=user_id)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=[{"msg": "A user with this id does not exist."}],
    #     )

    # try:
    #     user.set_password(password_reset.new_password)
    #     db_session.commit()
    # except ValueError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=[{"msg": str(e)}],
    #     ) from e

    # return user
    ...


@user_router.post("/update-email", response_model=UserReadSimple)
async def update_email(data_in: UpdateEmailUserInput, current_user: CurrentUser):
    """Update a user email."""
    user = await user_service.get(user_id=current_user.id)
    if not user:
        raise ResourceNotFoundException(
            "A subject with this id does not exist.")
    return await user_service.update(user=user, user_in=UserUpdate(
        email=data_in.email
    ))


@user_router.post("/change-password", response_model=UserReadSimple)
async def change_password(data_in: ChangePasswordUserInput, current_user: CurrentUser):
    """Change user password"""
    ...
