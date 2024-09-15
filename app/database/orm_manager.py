from typing import List, Sequence

from sqlalchemy import select

from app.database.db import db_manager, get_session, DatabaseSessionManager
from app.database.models.user_models import AbstractModel, UsersModel


class ORMManager(DatabaseSessionManager):
    def __init__(self) -> None:
        super().__init__()
        self.init()

    async def create_table(self) -> None:
        async with self.connect() as connection:
            await connection.run_sync(UsersModel.metadata.drop_all)
            await connection.run_sync(UsersModel.metadata.create_all)

    async def create_user(
            self, user_id: int, username: str, telefon: str
    ):
        async with self.session() as session:
            user = UsersModel(
                user_id=user_id,
                username=username,
                telefon=telefon
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    async def get_user(self, user_id: int) -> UsersModel:
        async with self.session() as session:
            user = await session.execute(
                select(UsersModel).where(UsersModel.user_id == user_id)
            )
            return user.scalars().one()

    async def get_users(self) -> Sequence[UsersModel]:
        async with self.session() as session:
            users = await session.execute(
                select(UsersModel)
            )
            return users.scalars().all()

    async def clear_table(self) -> None:
        async with self.connect() as connection:
            await connection.run_sync(UsersModel.metadata.drop_all)
            await connection.run_sync(UsersModel.metadata.create_all)


orm_manager = ORMManager()
