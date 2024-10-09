from sqlalchemy import select, update, delete  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore

from common.db.database import Session
from gym_app.models.models_sqlalchemy import User


class UserRepository:
    @staticmethod
    def get_all_users():
        query = select(User)
        result = Session.execute(query).scalars().all()
        return result

    @staticmethod
    def get_user(user_id):
        query = select(User).filter(User.id == user_id)
        result = Session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    def create_user(data):
        user = User(
            username=data.get("username"),
        )
        user.set_password(data.get("password"))
        Session.add(user)
        return user

    @staticmethod
    def update_user(user_id, data):
        user = Session.execute(select(User).filter(User.id == user_id)).scalar_one_or_none()

        if not user:
            return None

        if 'password' in data:
            user.set_password(data.pop('password'))

        for key, value in data.items():
            setattr(user, key, value)

        Session.add(user)
        return user

    @staticmethod
    def delete_user(user_id):
        query = delete(User).where(User.id == user_id)
        Session.execute(query)
        return True
