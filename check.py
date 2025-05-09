import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Genre, Movie, Review, User
from managers  import GenreManager
from managers  import MovieManager
from managers  import ReviewManager
from managers import UserManager

# Create an in-memory SQLite database for testing
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create all tables
        Base.metadata.create_all(engine)
        self.session = Session()
        self.genre_manager = GenreManager(self.session)
        self.movie_manager = MovieManager(self.session)
        self.review_manager = ReviewManager(self.session)
        self.user_manager = UserManager(self.session)

    def tearDown(self):
        # Drop all tables
        Base.metadata.drop_all(engine)
        self.session.close()

    def test_database_operations(self):
        # Create a genre
        genre = self.genre_manager.create(name="Action")
        self.assertIsNotNone(genre.id)

        # Create a user
        user = self.user_manager.create(name="Mobin Mojiri", email="Mobinmojiri1234@gmail.com")
        self.assertIsNotNone(user.id)

        # Create a movie
        movie = self.movie_manager.create(title="Inception", release_year=2010)
        self.assertIsNotNone(movie.id)

        # Add genre to movie
        movie = self.movie_manager.add_genre(movie_id=movie.id, genre=genre)
        self.assertIn(genre, movie.genres)

        # Create a review
        review = self.review_manager.create(movie_id=movie.id, user_id=user.id, rating=5, comment="Great movie!")
        self.assertIsNotNone(review.id)

        # Get movie by ID
        retrieved_movie = self.movie_manager.get(movie_id=movie.id)
        self.assertEqual(retrieved_movie.title, "Inception")

        # Get user by ID
        retrieved_user = self.user_manager.get(user_id=user.id)
        self.assertEqual(retrieved_user.name, "Mobin Mojiri")

        # Get genre by name
        retrieved_genre = self.genre_manager.get_genre_by_name(name="Action")
        self.assertEqual(retrieved_genre.name, "Action")

        # Get reviews for a movie
        reviews = self.movie_manager.get_reviews(movie_id=movie.id)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].rating, 5)

        # Get average rating for a movie
        avg_rating = self.movie_manager.get_average_rating(movie_id=movie.id)
        self.assertEqual(avg_rating, 5.0)

        # Get latest reviews for a movie
        latest_reviews = self.review_manager.get_latest_reviews_for_movie_by_time(movie_id=movie.id, limit=1)
        self.assertEqual(len(latest_reviews), 1)
        self.assertEqual(latest_reviews[0].rating, 5)

        # Get highest rated reviews for a movie
        highest_rated_reviews = self.review_manager.get_highest_rated_reviews(movie_id=movie.id, limit=1)
        self.assertEqual(len(highest_rated_reviews), 1)
        self.assertEqual(highest_rated_reviews[0].rating, 5)

        # Get average rating by user
        avg_ratings_by_user = self.review_manager.get_average_rating_by_user()
        self.assertEqual(len(avg_ratings_by_user), 1)
        self.assertEqual(avg_ratings_by_user[0][0], user.id)
        self.assertEqual(avg_ratings_by_user[0][1], 5.0)

        # Get most active users
        most_active_users = self.user_manager.get_most_active_users(limit=1)
        self.assertEqual(len(most_active_users), 1)
        self.assertEqual(most_active_users[0][0], user.id)
        self.assertEqual(most_active_users[0][1], 1)

if __name__ == '__main__':
    unittest.main()