from unittest.mock import MagicMock
import pytest

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService
from setup_db import db

@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    alan = Director(id=1, name='alan')
    bert = Director(id=2, name='bert')
    carl = Director(id=3, name='carl')

    director_dao.get_one = MagicMock(return_value=alan)
    director_dao.get_all = MagicMock(return_value=[alan, bert, carl])
    director_dao.create = MagicMock(return_value=Director(id=4))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao

class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        data = {'name': 'dany'}
        director = self.director_service.create(data)
        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        data = {
            'id': 3,
            'name': 'carl'
        }
        self.director_service.update(data)
