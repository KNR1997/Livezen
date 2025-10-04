from typing import List, Optional, Tuple
from tortoise.expressions import Q

from .models import LivezenUser


class UserRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[LivezenUser]]:
        # Use default if no search
        query = LivezenUser.filter(search) if search else LivezenUser.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs, ) -> LivezenUser:
        user = await LivezenUser.create(**kwargs)
        return user

    async def get(
        self, 
        prefetch: Optional[List[str]] = None, 
        **filters
    ) -> Optional[LivezenUser]:
        if prefetch:
            return await LivezenUser.filter(**filters).prefetch_related(*prefetch).first()
        else:
            return await LivezenUser.filter(**filters).first()

    async def list(self) -> List[LivezenUser]:
        return await LivezenUser.all()

    async def update(self, LivezenUser: LivezenUser, **kwargs) -> LivezenUser:
        for key, value in kwargs.items():
            setattr(LivezenUser, key, value)
        await LivezenUser.save()
        return LivezenUser

    async def delete(self, LivezenUser_id: int) -> bool:
        LivezenUser = await self.get(id=LivezenUser_id)
        if not LivezenUser:
            return False
        await LivezenUser.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await LivezenUser.exists(**kwards)
