class AuthenticationException(Exception):
    def __init__(self, message="Invalid username or password."):
        super().__init__(message)
