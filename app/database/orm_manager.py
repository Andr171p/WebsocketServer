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
            if user:
                return user.scalars().one()
            else:
                raise Exception("User not found")

    async def get_users(self) -> Sequence[UsersModel]:
        async with self.session() as session:
            users = await session.execute(
                select(UsersModel)
            )
            return users.scalars().all()

    async def get_phone(self, user_id: int) -> str | None:
        async with self.session() as session:
            phone = await session.execute(
                select(UsersModel.telefon).where(UsersModel.user_id == user_id)
            )
            try:
                return phone.scalars().one()
            except Exception as _ex:
                print(_ex)

    async def replace_phone(self, user_id: int, phone: str) -> UsersModel | None:
        async with self.session() as session:
            user = await session.execute(
                select(UsersModel).where(UsersModel.user_id == user_id)
            )
            user = user.scalars().first()
            if user:
                user.telefon = phone
                await session.commit()
                return user
            else:
                raise Exception("User not found")

    async def clear_table(self) -> None:
        async with self.connect() as connection:
            await connection.run_sync(UsersModel.metadata.drop_all)
            await connection.run_sync(UsersModel.metadata.create_all)


orm_manager = ORMManager()
