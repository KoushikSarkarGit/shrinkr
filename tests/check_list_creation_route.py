import asyncio
# import httpx

from app.infrastructure.database.database import AsyncSessionLocal
from app.models.userModel import User


async def main():
    async with AsyncSessionLocal() as session:
        # Create a test user using your User model's required fields.
        user = User(email="shrinkr-test@example.com", password_hash="test-password-hash")

        session.add(user)
        await session.commit()
        await session.refresh(user)

        user_id = str(user.id)

    # async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
    #     response = await client.post(
    #         "/api/v1/links",
    #         params={"user_id": user_id},
    #         json={
    #             "target_url": "https://example.com/products/123",
    #             "custom_alias": "test-product-123",
    #         },
    #     )

    #     print("Status:", response.status_code)
    #     print("Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
