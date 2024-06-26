#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        original_count = len(models.storage.all())
        new_state = State(name="California")
        new_state.save()
        new_city = City(name="San Francisco", state_id=new_state.id)
        new_city.save()
        self.assertEqual(len(models.storage.all()), original_count + 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        original_count = len(models.storage.all())
        new_state = State(name="Nevada")
        models.storage.new(new_state)
        models.storage.save()
        self.assertEqual(len(models.storage.all()), original_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        original_count = len(models.storage.all())
        new_state = State(name="Texas")
        new_state.save()
        self.assertEqual(len(models.storage.all()), original_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_method_obj(self):
        """Test the get method retrieves the correct object"""
        new_state = State(name="Florida")
        new_state.save()
        retrieved_state = models.storage.get(State, new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(new_state.id, retrieved_state.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_method_none(self):
        """Test the get method returns None for nonexistent object"""
        self.assertIsNone(models.storage.get(State, "doesnotexist"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """Test the count method counts all objects"""
        original_count = models.storage.count()
        new_state = State(name="Ohio")
        new_state.save()
        self.assertEqual(models.storage.count(), original_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_specific_class(self):
        """Test the count method counts objects of a specific class"""
        original_count = models.storage.count(State)
        new_state = State(name="Georgia")
        new_state.save()
        self.assertEqual(models.storage.count(State), original_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_specific_class_no_objects(self):
        """Test the count method counts zero when no objects of the class exist"""
        self.assertEqual(models.storage.count(Amenity), 0)


if __name__ == "__main__":
    unittest.main()

