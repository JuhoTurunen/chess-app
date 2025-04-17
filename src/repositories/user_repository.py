from services.db import SessionLocal
from entities.models import User


class UserRepository:
    def __init__(self):
        self.session = SessionLocal()

    def create_user(self, username):
        user = User(username=username)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user(self, username):
        return self.session.query(User).filter(User.username == username).first()
