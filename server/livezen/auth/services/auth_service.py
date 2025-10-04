from ..models import UserLogin, UserRegister, LivezenUser, UserCreate, UserUpdate
from ..repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, user_in: UserRegister) -> LivezenUser:
        return await self.repository.create(**user_in.model_dump())

    async def authenticate(self, credentials: UserLogin) -> LivezenUser | None:
        return await self.repository.get(email=credentials.email)
