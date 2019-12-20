import unittest
import os
from flask import current_app
from app import app


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()


    def tearDown(self):
        self.app_context.pop()


    def test_app_exists(self):
        """Test if the app exists """
        self.assertFalse(current_app is None)


    def test_enrollment_page(self):
        """Test the home page"""
        response = self.client.get('/enrollment')
        self.assertEqual(response.status_code, 200)

    def test_enroll(self):
        """Test the post response of enrollment"""
        response = self.client.post(
            '/enrollment?key=test', follow_redirects=True)
        # print(response.data)
        self.assertIn(b"You have enrolled successfully", response.data)

    def test_enroll_dublicate(self):
        """Test the post response of enrollment"""
        response = self.client.post(
            '/enrollment?key=test', follow_redirects=True)
        # print(response.data)
        self.assertIn(b"You aleardy enrolled in this program!", response.data)




if __name__ == '__main__':
    unittest.main()
