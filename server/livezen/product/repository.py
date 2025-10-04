from typing import List, Optional, Tuple
from tortoise.expressions import Q

from .models import Product


class ProductRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Product]]:
        # Use default if no search
        query = Product.filter(search) if search else Product.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> Product:
        product = await Product.create(**kwargs)
        return product

    async def get(self, **filters) -> Optional[Product]:
        return await Product.filter(**filters).first()

    async def list(self) -> List[Product]:
        return await Product.all()

    async def update(self, product: Product, **kwargs) -> Product:
        for key, value in kwargs.items():
            setattr(product, key, value)
        await product.save()
        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get(id=product_id)
        if not product:
            return False
        await product.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await Product.exists(**kwards)
