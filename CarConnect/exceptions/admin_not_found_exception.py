class AdminNotFoundException(Exception):
    def __init__(self, message="Admin not found."):
        super().__init__(message)
