from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models import Review




class ReviewManager:
    def __init__(self, session: Session):
        self.session = session

    def create(self, movie_id: int, user_id: int, rating: int, comment: str = None) -> Review:
        review = Review(
            rating = rating,
            comment = comment,
            movie_id = movie_id,
            user_id = user_id
        )
        self.session.add(review)
        self.session.commit()
        return review
    

    def get(self, review_id: int) -> Review | None:
        stmt = select(Review).where(Review.id == review_id)
        revById = self.session.execute(stmt).scalar_one_or_none()
        return revById


    def get_all(self):
        reviews = self.session.execute(select(Review)).scalars().all()
        return reviews


    def get_reviews_by_user(self, user_id: int):
        stmt = select(Review).where(Review.user_id == user_id)
        revByUserId = self.session.execute(stmt).scalar_one_or_none()
        return revByUserId
    

    def get_latest_reviews_for_movie_by_time(self, movie_id: int, limit: int = 5):
        stmt = select(Review).where(Review.movie_id == movie_id).order_by(Review.created_at.desc()).limit(limit)
        reviews = self.session.execute(stmt).scalars().all()
        return reviews

    def get_highest_rated_reviews(self, movie_id: int, limit: int = 5):
        stmt = select(Review).where(Review.movie_id == movie_id).order_by(Review.rating.desc()).limit(limit)
        reviews = self.session.execute(stmt).scalars().all()
        return reviews

    def get_average_rating_by_user(self):
        results = (
            self.session.query(
                Review.user_id,
                func.avg(Review.rating).label('average_rating')
            )
            .group_by(Review.user_id)
            .all()
        )
        return [(user_id, average_rating) for user_id, average_rating in results]


