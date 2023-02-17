from unittest.mock import MagicMock
import pytest

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService
from setup_db import db

@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    action = Genre(id=1, name='action')
    drama = Genre(id=2, name='drama')
    comedy = Genre(id=3, name='comedy')

    genre_dao.get_one = MagicMock(return_value=action)
    genre_dao.get_all = MagicMock(return_value=[action, drama, comedy])
    genre_dao.create = MagicMock(return_value=Genre(id=4))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao

class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id == 1

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        data = {'name': 'horror'}
        genre = self.genre_service.create(data)
        assert genre.id is not None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        data = {
            'id': 3,
            'name': 'carl'
        }
        self.genre_service.update(data)
