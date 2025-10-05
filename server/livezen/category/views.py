from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from livezen.exceptions import ConflictException, ResourceNotFoundException

from .models import CategoryCreate, CategoryPagination, CategoryRead, CategoryReadSimple, CategoryUpdate
from .repository import CategoryRepository
from .service import CategoryService


router = APIRouter()
service = CategoryService(CategoryRepository())


@router.get("", response_model=CategoryPagination)
async def paginated_categorys(
    page: int = Query(1, description="Page Number"),
    limit: int = Query(10, description="Items Per Page"),
    search: Optional[str] = Query("", description="Subject Name for Search"),
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

    total, data = await service.paginated(page=page, page_size=limit, search=q)
    return CategoryPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        perPage=limit,
        total=total,
    )


@router.get("/{slug}", response_model=CategoryRead)
async def get_category(slug: str):
    """Get a category by its slug."""
    category = await service.get_by_slug(slug)
    return category


@router.post("", response_model=CategoryReadSimple)
async def create_category(category_in: CategoryCreate):
    """Create a new category."""
    if await service.get_by_name(name=category_in.name):
        raise ConflictException(
            "Category with this name already exists", field="name")
    return await service.create(category_in)


@router.put("/{category_id}", response_model=CategoryReadSimple)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate
):
    """Update a category by its id."""
    category = await service.get(category_id=category_id)
    if not category:
        raise ResourceNotFoundException(
            "A category with this id does not exist.")
    if category_in.name != category.name:
        if await service.get_by_name(name=category_in.name):
            raise ConflictException(
                "Category with this name already exists", field="name")
    return await service.update(category=category, category_in=category_in)


@router.delete("/{category_id}", response_model=None)
async def delete_category(category_id: int):
    """Delete a category, returning only an HTTP 200 OK if successful."""
    return await service.delete(category_id)
