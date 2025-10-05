from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from livezen.exceptions import ConflictException, ResourceNotFoundException

from .models import TagCreate, TagPagination, TagRead, TagReadSimple, TagUpdate
from .repository import TagRepository
from .service import TagService


router = APIRouter()
service = TagService(TagRepository())


@router.get("", response_model=TagPagination)
async def paginated_tags(
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

                # ✅ Support nested related lookups like 'type.slug'
                field_path = field.replace(".", "__")

                # Build lookup dynamically
                lookup = {f"{field_path}__icontains": value}
                condition = Q(**lookup)

                if searchJoin.lower() == "or":
                    q |= condition
                else:
                    q &= condition
            except ValueError:
                continue  # skip invalid filter format

    total, data = await service.paginated(page=page, page_size=limit, search=q)
    return TagPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        perPage=limit,
        total=total,
    )


@router.get("/{slug}", response_model=TagRead)
async def get_tag(slug: str):
    """Get a tag by its slug."""
    tag = await service.get_by_slug(slug)
    return tag


@router.post("", response_model=TagReadSimple)
async def create_tag(tag_in: TagCreate):
    """Create a new tag."""
    if await service.get_by_name(name=tag_in.name):
        raise ConflictException(
            "Tag with this name already exists", field="name")
    return await service.create(tag_in)


@router.put("/{tag_id}", response_model=TagReadSimple)
async def update_tag(
    tag_id: int,
    tag_in: TagUpdate
):
    """Update a tag by its id."""
    tag = await service.get(tag_id=tag_id)
    if not tag:
        raise ResourceNotFoundException(
            "A tag with this id does not exist.")
    if tag_in.name != tag.name:
        if await service.get_by_name(name=tag_in.name):
            raise ConflictException(
                "Tag with this name already exists", field="name")
    return await service.update(tag=tag, tag_in=tag_in)


@router.delete("/{tag_id}", response_model=None)
async def delete_tag(tag_id: int):
    """Delete a tag, returning only an HTTP 200 OK if successful."""
    return await service.delete(tag_id)
