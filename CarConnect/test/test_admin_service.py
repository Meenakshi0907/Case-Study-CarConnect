import unittest
from unittest.mock import MagicMock
from CarConnect.entity.admin import Admin
from CarConnect.dao.admin_service import AdminService
from CarConnect.exceptions.admin_not_found_exception import AdminNotFoundException
from CarConnect.exceptions.invalid_input_exception import InvalidInputException
from CarConnect.exceptions.database_connection_exception import DatabaseConnectionException

class TestAdminService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = AdminService(self.mock_db)

    # --- get_admin_by_id ---
    def test_get_admin_by_id_valid(self):
        self.mock_db.fetch_query.return_value = [("1", "John", "Doe")]
        self.service.get_admin_by_id("1")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_admin_by_id_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.get_admin_by_id("abc")

    def test_get_admin_by_id_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(AdminNotFoundException):
            self.service.get_admin_by_id("999")

    def test_get_admin_by_id_db_error(self):
        self.mock_db.fetch_query.side_effect = DatabaseConnectionException("DB error")
        with self.assertRaises(DatabaseConnectionException):
            self.service.get_admin_by_id("1")

    # --- get_admin_by_username ---
    def test_get_admin_by_username_valid(self):
        self.mock_db.fetch_query.return_value = [("admin1", "Admin")]
        self.service.get_admin_by_username("admin1")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_admin_by_username_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.get_admin_by_username("")

    def test_get_admin_by_username_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(AdminNotFoundException):
            self.service.get_admin_by_username("ghostadmin")

    def test_get_admin_by_username_db_error(self):
        self.mock_db.fetch_query.side_effect = DatabaseConnectionException("DB error")
        with self.assertRaises(DatabaseConnectionException):
            self.service.get_admin_by_username("admin1")

    # --- register_admin ---
    def test_register_admin_valid(self):
        admin = Admin(None, "John", "Doe", "john@example.com", "1234567890", "admin1", "pass123", "super admin", None)
        self.service.register_admin(admin)
        self.mock_db.execute_query.assert_called_once()

    def test_register_admin_invalid_input_empty_fields(self):
        admin = Admin(None, "", "Doe", "john@example.com", "1234567890", "admin1", "pass123", "super admin", None)
        with self.assertRaises(InvalidInputException):
            self.service.register_admin(admin)

    def test_register_admin_invalid_input_phone(self):
        admin = Admin(None, "John", "Doe", "john@example.com", "12345", "admin1", "pass123", "super admin", None)
        with self.assertRaises(InvalidInputException):
            self.service.register_admin(admin)

    def test_register_admin_invalid_input_role(self):
        admin = Admin(None, "John", "Doe", "john@example.com", "1234567890", "admin1", "pass123", "manager", None)
        with self.assertRaises(InvalidInputException):
            self.service.register_admin(admin)

    def test_register_admin_db_error(self):
        self.mock_db.execute_query.side_effect = DatabaseConnectionException("Insert failed")
        admin = Admin(None, "John", "Doe", "john@example.com", "1234567890", "admin1", "pass123", "super admin", None)
        with self.assertRaises(DatabaseConnectionException):
            self.service.register_admin(admin)

    # --- update_admin ---
    def test_update_admin_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.update_admin("1", "John", "Smith", "johnsmith@example.com", "9876543210", "johnsmith", "super admin")
        self.mock_db.execute_query.assert_called_once()

    def test_update_admin_invalid_input_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_admin("abc", "John", "Smith", "email", "9876543210", "username", "super admin")

    def test_update_admin_invalid_input_phone(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_admin("1", "John", "Smith", "email", "phone", "username", "super admin")

    def test_update_admin_invalid_input_role(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_admin("1", "John", "Smith", "email", "9876543210", "username", "admin")

    def test_update_admin_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(AdminNotFoundException):
            self.service.update_admin("1", "John", "Smith", "email", "9876543210", "username", "super admin")

    def test_update_admin_db_error(self):
        self.mock_db.execute_query.side_effect = DatabaseConnectionException("Update failed")
        with self.assertRaises(DatabaseConnectionException):
            self.service.update_admin("1", "John", "Smith", "email", "9876543210", "username", "super admin")

    # --- delete_admin ---
    def test_delete_admin_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.delete_admin("1")
        self.mock_db.execute_query.assert_called_once()

    def test_delete_admin_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.delete_admin("abc")

    def test_delete_admin_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(AdminNotFoundException):
            self.service.delete_admin("999")

    def test_delete_admin_db_error(self):
        self.mock_db.execute_query.side_effect = DatabaseConnectionException("Delete failed")
        with self.assertRaises(DatabaseConnectionException):
            self.service.delete_admin("1")

if __name__ == "__main__":
    unittest.main()
