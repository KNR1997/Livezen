from typing import Any
from uuid import UUID

from livezen.auth.models import Profile

from ..repository import ProfileRepository, UserRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository, user_repository: UserRepository):
        self.repository = repository
        self.user_repository = user_repository

    async def create(self, user_id: UUID, data: dict[str, Any]) -> Profile:
        return await self.repository.create(user_id=user_id, **data)

    async def update(self, profile: Profile, data: dict[str, Any]) -> Profile:
        """Updates a profile."""
        return await self.repository.update(profile, **data)

    async def get_by_user(self, user_id: UUID) -> Profile | None:
        return await self.repository.get(user_id=user_id)
