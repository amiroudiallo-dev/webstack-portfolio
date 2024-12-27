#!/usr/bin/python3
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_status_endpoint(self):
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "API is running!"})

if __name__ == '__main__':
    unittest.main()
