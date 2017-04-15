import pytest
import unittest
from app import app

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    @pytest.mark.inject
    def test_successful_login(self):
        res = self.app.post("/", data=dict(vendor="Electrician", password="34c9b6ca63682155572447dbed32a8e6a91990982ec5b36a24c40dfe24595660"))
        self.assertTrue("Welcome" in str(res.data), msg="Login did not happen even with correct credentials")

    @pytest.mark.inject
    def test_invalid_credential_login(self):
        res = self.app.post("/", data=dict(vendor="Electrician", password="test"))
        self.assertTrue("Sorry" in str(res.data), msg="Login happened even with incorrect credentials")

    @pytest.mark.inject
    def test_injection(self):
        res = self.app.post("/", data=dict(vendor="Electrician", password="a' or 1=1; -- com"))
        self.assertFalse("Welcome" in str(res.data), msg="SQL injection exists in the application")