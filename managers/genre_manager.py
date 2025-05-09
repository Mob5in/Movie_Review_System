from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Genre


class GenreManager:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str) -> Genre:
        genre = Genre(
            name = name
        )
        self.session.add(genre)
        self.session.commit()
        return genre
        
    def get(self, genre_id: int) -> Genre | None:
        stmt = select(Genre).where(Genre.id == genre_id)
        genById = self.session.execute(stmt).scalar_one_or_none()
        return genById


    def get_all(self):
        genres = self.session.execute(select(Genre)).scalars().all()
        return genres

    def get_genre_by_name(self, name: str) -> Genre | None:
        stmt = select(Genre).where(Genre.name == name)
        genByName = self.session.execute(stmt).scalar_one_or_none()
        return genByName