from config import AUTH_TOKEN_SECRET
from exceptions import UnauthorizedError

class AuthService:
    def __init__(self, secret_token: str):
        self.secret_token = secret_token

    def authenticate(self, provided_token: str) -> bool:
        if provided_token != self.secret_token:
            raise UnauthorizedError("Invalid authentication token.")
        return True

    def authorize_role(self, user_role: str, required_roles: list) -> bool:
        # For now, a simplified placeholder.
        # In a real system, this would involve more complex role-based access control.
        if user_role in required_roles:
            return True
        return False
