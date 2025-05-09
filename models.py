
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass


class MovieGenre(Base):
    __tablename__ = "movie_genres"
    
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)



class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key= True)
    title: Mapped[str] = mapped_column(String(255), nullable= False)
    release_year: Mapped[int] = mapped_column(nullable= True)
    genres: Mapped[List["Genre"]] = relationship(secondary="movie_genres", back_populates="movies")

    reviews: Mapped[List['Review']] = relationship("Review", back_populates= "movie")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(String(255), nullable= False)
    email: Mapped[str] = mapped_column(String(255), nullable= False, unique= True)
    is_verified: Mapped[bool] = mapped_column(default= False, nullable= False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates='user')

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(String(255), unique= True, )
    movies: Mapped[List["Movie"]] = relationship(secondary="movie_genres", back_populates="genres")

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


    movie: Mapped["Movie"] = relationship("Movie", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")










