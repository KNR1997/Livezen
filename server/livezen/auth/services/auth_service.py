from ..models import UserLogin, UserRegister, LivezenUser, UserCreate, UserUpdate, hash_password
from ..repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, user_in: UserRegister) -> LivezenUser:
        hashed_password = hash_password(user_in.password)
        user_data = user_in.model_dump()
        user_data["password"] = hashed_password
        return await self.repository.create(**user_data)

    async def authenticate(self, credentials: UserLogin) -> LivezenUser | None:
        return await self.repository.get(email=credentials.email)
