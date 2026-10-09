import asyncio
import uuid

from sqlalchemy import select

from app.infrastructure.database.database import (
    AsyncSessionLocal,
    Base,
    engine,
)
from app.models import Link, User


async def main():
    try:
        # Temporary schema creation for this Day 3 checkpoint.
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    user = User(
                        email=f"test-{uuid.uuid4()}@example.com",
                        password_hash="temporary-test-hash",
                    )
                    session.add(user)
                    await session.flush()

                    link = Link(
                        user_id=user.id,
                        code=f"test-{uuid.uuid4().hex[:12]}",
                        target_url="https://example.com",
                    )
                    session.add(link)
                    await session.flush()

                    saved_user = await session.scalar(
                        select(User).where(User.id == user.id)
                    )
                    saved_link = await session.scalar(
                        select(Link).where(Link.id == link.id)
                    )

                    assert saved_user is not None
                    assert saved_link is not None
                    assert saved_link.user_id == saved_user.id

                    print("User created and queried successfully.")
                    print("Link created and queried successfully.")
                    print("User-Link relationship verified.")

                    # Roll back the test records; keep the tables.
                    await session.rollback()
            except Exception:
                await session.rollback()
                raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
