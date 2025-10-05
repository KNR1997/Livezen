import asyncio
from tortoise import Tortoise, run_async

from livezen.type.models import Type
from livezen.category.models import Category


async def seed():
    print("🌱 Starting database seeding...")

    # --- Example 1: Create Types ---
    grocery, _ = await Type.get_or_create(
        name="Grocery",
        slug="grocery",
        defaults={
            "translated_languages": ["en"],
            "banners": [],
            "promotional_sliders": [],
        }
    )

    await Type.get_or_create(
        name="Fruits",
        slug="fruits",
        parent=grocery
    )

    # --- Example 2: Create a Category ---
    await Category.get_or_create(
        name="Fresh Fruits",
        slug="fresh-fruits",
        type=grocery
    )

    print("✅ Seeding completed successfully.")


async def init():
    ...
    # await Tortoise.init(
    #     db_url="sqlite://db.sqlite3",  # update to match your DATABASE_URL
    #     modules={"models": ["app.models"]},
    # )
    # await Tortoise.generate_schemas()
    # await seed()
    # await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(init())
