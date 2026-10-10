from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.userModel import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Behavior	        session.scalar()	    execute and then scalar_one_or_none()
    # No match	        None	                None
    # One match	        Returns User	        Returns User
    # Multiple matches	Returns first result	Raises MultipleResultsFound

    async def get_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
