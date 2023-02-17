from unittest.mock import MagicMock
import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db

@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    saw_1 = Movie(id=1, title='saw_1', description='desc_1', trailer='trl_1', year=2004, rating=3, genre_id=1, director_id=1)
    saw_2 = Movie(id=2, title='saw_2', description='desc_2', trailer='trl_2', year=2005, rating=3, genre_id=1, director_id=1)
    saw_3 = Movie(id=3, title='saw_3', description='desc_3', trailer='trl_3', year=2006, rating=3, genre_id=1, director_id=1)

    movie_dao.get_one = MagicMock(return_value=saw_1)
    movie_dao.get_all = MagicMock(return_value=[saw_1, saw_2, saw_3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao

class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        data = {
            'title': 'saw_4',
            'description': 'desc_4',
            'trailer': 'trl_4',
            'year': 2007,
            'rating':3,
            'genre_id': 1,
            'director_id': 1
        }
        movie = self.movie_service.create(data)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        data = {
            'id': 3,
            'title': 'saw_4',
            'description': 'desc_4',
            'trailer': 'trl_4',
            'year': 2007,
            'rating':3,
            'genre_id': 1,
            'director_id': 1
        }
        self.movie_service.update(data)
