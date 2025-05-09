from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from models import Movie, Genre, Review


class MovieManager:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, title: str, release_year: int) -> Movie:
        movie = Movie(
            title = title,
            release_year = release_year,
        )
        self.session.add(movie)
        self.session.commit()
        return movie

    def get(self, movie_id: int) -> Movie | None:
        stmt = select(Movie).where(Movie.id == movie_id)
        movieById = self.session.execute(stmt).scalar_one_or_none()
        return movieById
    

    def get_all(self):
        movies = self.session.execute(select(Movie)).scalars().all()
        return movies
    

    def add_genre(self, movie_id: int, genre: Genre) -> Movie:
        movie = self.get(movie_id)

        if genre not in movie.genres:
            movie.genres.append(genre)
            self.session.commit()

        return movie

    def get_reviews(self, movie_id: int):
        movie = self.get(movie_id)

        return movie.reviews


    def get_average_rating(self, movie_id: int):
        movie = self.get(movie_id)
        
        if not movie.reviews:
            return None
        
        total = sum(review.rating for review in movie.reviews)
        return total / len(movie.reviews)
