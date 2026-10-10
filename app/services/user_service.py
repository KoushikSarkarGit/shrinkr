from app.repositories.user_repository import UserRepository
from app.models.userModel import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email)
