"""Test State module"""
import unittest
from flask import json
from api.v1.app import app
from api.v1.views.states import *


class TestState(unittest.TestCase):
    """Test cases for state.py module"""
    def setUp(self):
        """Runs at the start of the test"""
        self.app = app.test_client()

    def test_get_states_list(self):
        """Check the get states"""
        response = self.app.get('/api/v1/states/')
        # data = response.get_json()

        self.assertEqual(response.status_code, 200)

    def test_create_state(self):
        """Create a state"""
        state_data = {
            "name": "Kwara"
        }

        response = self.app.post(
            '/api/v1/states/',
            data=json.dumps(state_data),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 201)

        state_json = response.get_json()
        self.assertIsNotNone(state_json)

        # Test retrival, update and deleting of a test
        # Test  retrival of a test
        created_state_id = state_json.get("id")

        get_response = self.app.get(f'/api/v1/states/{created_state_id}')

        self.assertEqual(get_response.status_code, 200)

        retrieved_state = get_response.get_json()
        self.assertEqual(retrieved_state.get("name"), state_data.get("name"))

        # Test Update of a State
        update_data = {
            "name": "California is so cool"
        }

        update_response = self.app.put(
            f'/api/v1/states/{created_state_id}',
            data=json.dumps(update_data),
            content_type='application/json'
            )

        self.assertEqual(update_response.status_code, 200)

        retrieved_updated_state = update_response.get_json()
        self.assertNotEqual(
            retrieved_updated_state.get("name"),
            state_data.get("name")
            )

        # Test delete of a state
        del_response = self.app.delete(f'/api/v1/states/{created_state_id}')

        self.assertEqual(del_response.status_code, 200)

        retrieved_del_state = del_response.get_json()
        self.assertEqual(retrieved_del_state, {})

    if __name__ == '__main__':
        unittest.main()
