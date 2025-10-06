from typing import List, Tuple
from fastapi.security import OAuth2PasswordBearer
from tortoise.expressions import Q
from uuid import UUID


from ..models import LivezenUser, UserCreate, UserUpdate
from ..repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[LivezenUser]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def list_users(self) -> list[LivezenUser]:
        return await self.repository.list()

    async def get(self, user_id: UUID) -> LivezenUser | None:
        """Gets a user by id."""
        return await self.repository.get(id=user_id)

    async def get_by_name(self, name: str) -> LivezenUser | None:
        """Gets a user by name."""
        return await self.repository.get(name=name)

    async def get_by_email(self, email: str) -> LivezenUser | None:
        """Gets a user by email."""
        return await self.repository.get(email=email)

    async def create(self, user_in: UserCreate) -> LivezenUser:
        return await self.repository.create(**user_in.model_dump())

    async def get_or_create(self, email: str, user_in: UserCreate) -> LivezenUser:
        if email:
            instance = await self.repository.get(email=email)
        if instance:
            return instance
        return await self.repository.create(**user_in.model_dump())

    async def update(self, user: LivezenUser, user_in: UserUpdate) -> LivezenUser:
        """Updates a user."""
        return await self.repository.update(user, **user_in.model_dump(exclude_unset=True))

    async def delete(self, user_id: int) -> bool:
        """Deletes a user."""
        return await self.repository.delete(user_id)
