class DatabaseConnectionException(Exception):
    def __init__(self, message="Unable to connect to the database."):
        super().__init__(message)
