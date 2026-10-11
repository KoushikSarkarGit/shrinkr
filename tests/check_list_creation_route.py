import asyncio
from sqlalchemy import select

from app.infrastructure.database.database import AsyncSessionLocal
from app.models.userModel import User


async def main():
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User.id).limit(1))

        if user is None:
            print("No user found. Create a test user first.")
            return

        user_id = str(user)

    print(f"Testing with user_id={user_id}")

    import httpx

    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/api/v1/links",
            params={"user_id": user_id},
            json={
                "target_url": "https://example.com/products/123",
                "custom_alias": "test-product-123",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
