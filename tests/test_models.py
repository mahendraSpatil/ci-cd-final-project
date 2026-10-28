"""
Test cases for Account Model
"""
import unittest
from service import app
from service.models import Account, DataValidationError, db

ACCOUNT_DATA = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "address": "123 Main Street, New York, NY",
    "phone_number": "555-123-4567",
}


class TestAccountModel(unittest.TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    def setUp(self):
        """This runs before each test"""
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """This runs after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_an_account(self):
        """Test creating an Account"""
        with app.app_context():
            account = Account()
            account.deserialize(ACCOUNT_DATA)
            account.create()
            self.assertIsNotNone(account.id)
            found = Account.find(account.id)
            self.assertEqual(found.name, ACCOUNT_DATA["name"])
            self.assertEqual(found.email, ACCOUNT_DATA["email"])

    def test_update_an_account(self):
        """Test updating an Account"""
        with app.app_context():
            account = Account()
            account.deserialize(ACCOUNT_DATA)
            account.create()
            account.name = "Jane Doe"
            account.update()
            found = Account.find(account.id)
            self.assertEqual(found.name, "Jane Doe")

    def test_delete_an_account(self):
        """Test deleting an Account"""
        with app.app_context():
            account = Account()
            account.deserialize(ACCOUNT_DATA)
            account.create()
            self.assertEqual(len(Account.all()), 1)
            account.delete()
            self.assertEqual(len(Account.all()), 0)

    def test_serialize_an_account(self):
        """Test serialization of an Account"""
        account = Account()
        account.deserialize(ACCOUNT_DATA)
        serial_data = account.serialize()
        self.assertEqual(serial_data["name"], ACCOUNT_DATA["name"])
        self.assertEqual(serial_data["email"], ACCOUNT_DATA["email"])

    def test_deserialize_bad_data(self):
        """Test deserialization with missing data"""
        account = Account()
        with self.assertRaises(DataValidationError):
            account.deserialize({"name": "Bad"})

    def test_repr(self):
        """Test string representation of Account"""
        account = Account()
        account.name = "Test"
        account.id = 1
        self.assertEqual(repr(account), "<Account Test id=[1]>")
