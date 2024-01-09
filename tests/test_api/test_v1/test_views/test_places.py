"""Test Place module"""
import unittest
from flask import json
from api.v1.app import app
from api.v1.views.places import *
from models.city import City
from models.place import Place
from api.v1.views.cities import *


class TestState(unittest.TestCase):
    """Test cases for state.py module"""
    def setUp(self):
        """Runs at the start of the test"""
        self.app = app.test_client()

    def test_get_places_list(self):
        """Check the get states"""
        pass
        # response = self.app.get(
        #     '/api/v1/cities/valid_city_id/places'
        #     )

        # # data = response.get_json()
        # self.assertEqual(response.status_code, 200)

    if __name__ == '__main__':
        unittest.main()
