from CarConnect.exceptions.admin_not_found_exception import AdminNotFoundException
from CarConnect.exceptions.invalid_input_exception import InvalidInputException
from CarConnect.exceptions.database_connection_exception import DatabaseConnectionException

class AdminService:
    def __init__(self, db):
        self.db = db

    def get_admin_by_id(self, admin_id):
        if not admin_id.isdigit():
            raise InvalidInputException("Admin ID must be an integer.")
        try:
            query = "SELECT * FROM Admin WHERE AdminID = %s"
            row = self.db.fetch_query(query, (admin_id,))
            if not row:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found.")
            print("The Admin is:",row)
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Database error: {str(e)}")

    def get_admin_by_username(self, username):
        if not isinstance(username, str) or not username.strip():
            raise InvalidInputException("Username must be a non-empty string.")
        try:
            query = "SELECT * FROM Admin WHERE Username = %s"
            row = self.db.fetch_query(query, (username,))
            if not row:
                raise AdminNotFoundException(f"No admin found with username: {username}")
            print("The user is:",row)
        except AdminNotFoundException:
            raise AdminNotFoundException(f"No admin found with username: {username}")
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Database error: {str(e)}")

    def register_admin(self, admin):
        if not all([admin.first_name.strip(), admin.last_name.strip(), admin.email.strip(),
                    admin.phone.strip(), admin.username.strip(), admin.password.strip(), admin.role.strip()]):
            raise InvalidInputException("Admin fields must not be empty.")

        if not (admin.phone.isdigit() and len(admin.phone) == 10):
            raise InvalidInputException("Phone number must be a 10-digit number.")

        if admin.role not in ['super admin', 'fleet manager']:
            raise InvalidInputException("Role must be 'super admin' or 'fleet manager'.")
        try:
            query = """
                INSERT INTO Admin (FirstName, LastName, Email, PhoneNumber, Username, Password, Role, JoinDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """
            values = (
                admin.first_name, admin.last_name, admin.email,
                admin.phone, admin.username, admin.password, admin.role
            )
            self.db.execute_query(query, values)
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Failed to register admin: {str(e)}")

    def update_admin(self, admin_id, first_name, last_name,email,phone,username,role):
        if not admin_id.isdigit():
            raise InvalidInputException("Admin ID must be an integer.")

        if not (phone.isdigit() and len(phone) == 10):
            raise InvalidInputException("Phone number must be a 10-digit number.")

        if role not in ['super admin', 'fleet manager']:
            raise InvalidInputException("Role must be 'super admin' or 'fleet manager'.")
        try:
            query = ("UPDATE Admin SET FirstName = %s, LastName = %s,"
                     "Email = %s, PhoneNumber = %s, username = %s, role = %s WHERE AdminID = %s")
            result = self.db.execute_query(query, (first_name, last_name,email, phone,username,role, admin_id))
            if result == 0:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found.")
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Failed to update admin: {str(e)}")

    def delete_admin(self, admin_id):
        if not admin_id.isdigit():
            raise InvalidInputException("Admin ID must be an integer.")
        try:
            query = "DELETE FROM Admin WHERE AdminID = %s"
            result = self.db.execute_query(query, (admin_id,))
            if result == 0:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found.")
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Failed to delete admin: {str(e)}")
