from typing import Optional
from fastapi import APIRouter, Depends, Query
from tortoise.expressions import Q

from livezen.auth.permissions import AdminPermission, PermissionsDependency
from livezen.exceptions import ConflictException, ResourceNotFoundException

from .models import ProductCreate, ProductPagination, ProductRead, ProductUpdate
from .repository import ProductRepository
from .service import ProductService


router = APIRouter()
service = ProductService(ProductRepository())


@router.get("", response_model=ProductPagination)
async def paginated_products(
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
    search: Optional[str] = Query("", description="Product Name for Search"),
    searchJoin: str = Query(
        "and", description="'and' or 'or' join for multiple search conditions"),
):
    q = Q()
    if search:
        # Example: search="name:english;status:active"
        filters = search.split(";")
        for f in filters:
            try:
                field, value = f.split(":", 1)
                lookup = {f"{field}__icontains": value}
                condition = Q(**lookup)
                if searchJoin.lower() == "or":
                    q |= condition
                else:
                    q &= condition
            except ValueError:
                continue  # skip invalid filter format

    total, data = await service.paginated(page=page, page_size=page_size, search=q)
    return ProductPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int):
    """Get a product by its id."""
    product = await service.get(product_id)
    return product


@router.post(
    "",
    response_model=ProductRead,
    # dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
async def create_product(product_in: ProductCreate):
    """Create a new product."""
    if await service.get_by_name(name=product_in.name):
        raise ConflictException(
            "Product with this name already exists", field="name")
    return await service.create(product_in)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_in: ProductUpdate
):
    """Update a product by its id."""
    product = await service.get(product_id=product_id)
    if not product:
        raise ResourceNotFoundException(
            "A product with this id does not exist.")
    if product_in.name != product.name:
        if await service.get_by_name(name=product_in.name):
            raise ConflictException(
                "Product with this name already exists", field="name")
    return await service.update(product=product, product_in=product_in)


@router.delete("/{product_id}", response_model=None)
async def delete_product(product_id: int):
    """Delete a product, returning only an HTTP 200 OK if successful."""
    return await service.delete(product_id)
