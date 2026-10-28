"""
Account Service API Test Suite
"""
import unittest
from service import app
from service.models import db, Account
from service.common import status

BASE_URL = "/accounts"
ACCOUNT_PAYLOAD = {
    "name": "Jane Smith",
    "email": "janesmith@example.com",
    "address": "456 Oak Avenue, Metropolis, NY",
    "phone_number": "555-987-6543",
}


class TestAccountService(unittest.TestCase):
    """Account Service Test Cases"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    def setUp(self):
        """Run before each test"""
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Run after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        """Test the home page endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Account REST API Service")

    def test_health(self):
        """Test the health check endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """Test creating a new Account"""
        response = self.client.post(
            BASE_URL,
            json=ACCOUNT_PAYLOAD,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        new_account = response.get_json()
        self.assertEqual(new_account["name"], ACCOUNT_PAYLOAD["name"])
        self.assertEqual(new_account["email"], ACCOUNT_PAYLOAD["email"])

    def test_get_account(self):
        """Test reading an existing Account"""
        resp = self.client.post(
            BASE_URL,
            json=ACCOUNT_PAYLOAD,
            content_type="application/json",
        )
        account_id = resp.get_json()["id"]
        response = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], ACCOUNT_PAYLOAD["name"])

    def test_get_account_not_found(self):
        """Test reading an Account that does not exist"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_accounts(self):
        """Test listing all accounts"""
        self.client.post(BASE_URL, json=ACCOUNT_PAYLOAD, content_type="application/json")
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)

    def test_update_account(self):
        """Test updating an existing Account"""
        resp = self.client.post(BASE_URL, json=ACCOUNT_PAYLOAD, content_type="application/json")
        account_id = resp.get_json()["id"]
        updated_payload = dict(ACCOUNT_PAYLOAD)
        updated_payload["name"] = "Jane Updated"
        response = self.client.put(
            f"{BASE_URL}/{account_id}",
            json=updated_payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Jane Updated")

    def test_update_account_not_found(self):
        """Test updating an Account that does not exist"""
        response = self.client.put(
            f"{BASE_URL}/0",
            json=ACCOUNT_PAYLOAD,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        """Test deleting an Account"""
        resp = self.client.post(BASE_URL, json=ACCOUNT_PAYLOAD, content_type="application/json")
        account_id = resp.get_json()["id"]
        response = self.client.delete(f"{BASE_URL}/{account_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unsupported_media_type(self):
        """Test sending unsupported media type"""
        response = self.client.post(BASE_URL, data="text string", content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """Test calling endpoint with disallowed method"""
        response = self.client.delete(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
