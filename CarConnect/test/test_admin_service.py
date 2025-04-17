import unittest
from unittest.mock import MagicMock
from CarConnect.dao.admin_service import AdminService
from CarConnect.entity.admin import Admin
from CarConnect.exceptions.admin_not_found_exception import AdminNotFoundException
from CarConnect.exceptions.invalid_input_exception import InvalidInputException
from CarConnect.exceptions.authentication_exception import AuthenticationException

class TestAdminService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.admin_service = AdminService(self.mock_db)

    def test_get_admin_by_id_success(self):
        self.mock_db.fetch_query.return_value = [(1, "John", "john@example.com", "johnadmin", "pass123", "super admin", "2025-04-01")]
        self.admin_service.get_admin_by_id("1")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_admin_by_id_invalid(self):
        with self.assertRaises(InvalidInputException):
            self.admin_service.get_admin_by_id("abc")

    def test_get_admin_by_id_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(AdminNotFoundException):
            self.admin_service.get_admin_by_id("999")

    def test_register_admin_success(self):
        admin = Admin(None, "Jane", "Doe", "jane@example.com", "9876543210", "janeadmin", "secret", "fleet manager", None)
        self.admin_service.register_admin(admin)
        self.mock_db.execute_query.assert_called_once()

    def test_register_admin_invalid_phone(self):
        admin = Admin(None, "Jane", "Doe", "jane@example.com", "12345", "janeadmin", "secret", "fleet manager", None)
        with self.assertRaises(InvalidInputException):
            self.admin_service.register_admin(admin)

    def test_update_admin_success(self):
        self.mock_db.execute_query.return_value = 1
        self.admin_service.update_admin("1", "Jane", "Smith", "jane@smith.com", "9876543210", "janesmith", "super admin")
        self.mock_db.execute_query.assert_called_once()

    def test_update_admin_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(AdminNotFoundException):
            self.admin_service.update_admin("2", "Test", "User", "test@user.com", "1234567890", "testuser", "fleet manager")

    def test_delete_admin_success(self):
        self.mock_db.execute_query.return_value = 1
        self.admin_service.delete_admin("1")
        self.mock_db.execute_query.assert_called_once()

    def test_delete_admin_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(AdminNotFoundException):
            self.admin_service.delete_admin("99")

    def test_authenticate_admin_success(self):
        self.mock_db.fetch_query.return_value = [("John", "super admin")]
        role = self.admin_service.authenticate_admin("johnadmin", "pass123")
        self.assertEqual(role, "super admin")

    def test_authenticate_admin_failure(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(AuthenticationException):
            self.admin_service.authenticate_admin("wronguser", "wrongpass")


if __name__ == '__main__':
    unittest.main()
