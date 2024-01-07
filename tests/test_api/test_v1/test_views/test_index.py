#!/usr/bin/python3
"""Test Index module"""
import unittest
from unittest.mock import patch
from api.v1.app import app
# from api.v1.views.index import retrieve_object_number


class TestIndex(unittest.TestCase):
    """Test cases for index.py module"""
    def setUp(self):
        """Runs at the start of the test"""
        self.app = app.test_client()

    @patch('api.v1.views.index.storage.count')
    def test_retrieve_object_number(self, mock_count):
        """Retrieves the number of each objects by type"""
        mock_count.return_value = 47

        response = self.app.get('/api/v1/stats')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['amenities'], 47)


if __name__ == '__main__':
    unittest.main()
