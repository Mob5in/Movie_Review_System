from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models import Review, User


class UserManager:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, email: str) -> User:
        user = User(
            name = name,
            email = email
        )
        self.session.add(user)
        self.session.commit()
        return user

    def get(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        userById = self.session.execute(stmt).scalar_one_or_none()
        return userById


    def get_all(self):
        users = self.session.execute(select(User)).scalars().all()
        return users
        
    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        userByEmail = self.session.execute(stmt).scalar_one_or_none()
        return userByEmail

    def get_most_active_users(self, limit=5):
        stmt = (
        select(Review.user_id, func.count(Review.id).label('review_count'))
        .group_by(Review.user_id)
        .order_by(func.count(Review.id).desc())
        .limit(limit)
        )
        return self.session.execute(stmt).all()