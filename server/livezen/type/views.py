from typing import List, Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from livezen.exceptions import ConflictException, ResourceNotFoundException

from .models import TypeCreate, TypePagination, TypeRead, TypeUpdate
from .repository import TypeRepository
from .service import TypeService


router = APIRouter()
service = TypeService(TypeRepository())

# Mapping of special search keys → list of model fields to search
SEARCH_FIELD_MAPPINGS = {
    "name": ["first_name", "last_name", "phone_number", "nic_number"],
}


# @router.get("", response_model=TypePagination)
# async def paginated_types(
#     page: int = Query(1, description="Page Number"),
#     page_size: int = Query(10, description="Items Per Page"),
#     search: Optional[str] = Query("", description="Subject Name for Search"),
#     searchJoin: str = Query(
#         "and", description="'and' or 'or' join for multiple search conditions"),
# ):
#     q = Q()
#     if search:
#         # Example: search="name:english;status:active"
#         filters = search.split(";")
#         for f in filters:
#             try:
#                 field, value = f.split(":", 1)

#                 if field in SEARCH_FIELD_MAPPINGS:
#                     # Build OR condition for all mapped fields
#                     condition = Q()
#                     for mapped_field in SEARCH_FIELD_MAPPINGS[field]:
#                         condition |= Q(**{f"{mapped_field}__icontains": value})
#                 else:
#                     # Normal single-field search
#                     lookup = {f"{field}__icontains": value}
#                     condition = Q(**lookup)

#                 if searchJoin.lower() == "or":
#                     q |= condition
#                 else:
#                     q &= condition
#             except ValueError:
#                 continue  # skip invalid filter format

#     total, data = await service.paginated(page=page, page_size=page_size, search=q)
#     return TypePagination(
#         data=data,
#         itemsPerPage=10,
#         page=page,
#         page_size=page_size,
#         total=total,
#     )

@router.get("", response_model=List[TypeRead])
async def list():
    """Get type list."""
    type_list = await service.list()
    return type_list


@router.get("/{slug}", response_model=TypeRead)
async def get_type(slug: str):
    """Get a type by its slug."""
    type = await service.get_by_slug(slug)
    return type


@router.post("", response_model=TypeRead)
async def create_type(type_in: TypeCreate):
    """Create a new type."""
    if await service.get_by_name(name=type_in.name):
        raise ConflictException(
            "Type with this name already exists", field="name")
    return await service.create(type_in)


@router.put("/{type_id}", response_model=TypeRead)
async def update_type(
    type_id: int,
    type_in: TypeUpdate
):
    """Update a type by its id."""
    type = await service.get(type_id=type_id)
    if not type:
        raise ResourceNotFoundException(
            "A type with this id does not exist.")
    if type_in.name != type.name:
        if await service.get_by_name(name=type_in.name):
            raise ConflictException(
                "Type with this name already exists", field="name")
    return await service.update(type=type, type_in=type_in)


@router.delete("/{type_id}", response_model=None)
async def delete_type(type_id: int):
    """Delete a type, returning only an HTTP 200 OK if successful."""
    return await service.delete(type_id)
