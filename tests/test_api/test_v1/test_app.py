#!/usr/bin/python3
"""Test App module"""
import unittest
from api.v1.app import app


class TestApp(unittest.TestCase):
    """Test cases for app.py module"""
    def setUp(self):
        """Runs at the start of the test"""
        self.app = app.test_client()

    def test_get_status(self):
        """Check if the status of the API is 200"""
        response = self.app.get('/api/v1/status')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'OK')

    def test_page_not_found(self):
        """Checks if the 404 route works whwn an invalid request is made"""
        response = self.app.get('/api/v1/not_found')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found')


if __name__ == '__main__':
    unittest.main()
