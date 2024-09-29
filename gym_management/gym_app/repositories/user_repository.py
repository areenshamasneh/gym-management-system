from sqlalchemy import select, update, delete  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore
from werkzeug.security import generate_password_hash

from common.db.database import Session
from gym_app.models.models_sqlalchemy import User

class UserRepository:
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
        if 'password' in data:
            data['hashed_password'] = generate_password_hash(data.pop('password'))

        query = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .execution_options(synchronize_session="evaluate")
        )
        Session.execute(query)
        return Session.execute(select(User).filter(User.id == user_id)).scalar_one_or_none()

    @staticmethod
    def delete_user(user_id):
        query = delete(User).where(User.id == user_id)
        Session.execute(query)
        return True

    def authenticate_user(self, username: str, password: str):
        user = Session.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            return user
        return None