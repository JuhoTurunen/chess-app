from persistence.session import SessionLocal
from persistence.models.user import User


class UserRepository:
    """Handles database operations for User entities."""

    def __init__(self):
        """Initializes a UserRepository with a new database session."""
        self._session = SessionLocal()

    def create_user(self, username):
        """Creates a new user.

        Args:
            username: String for username.

        Returns:
            User object.
        """
        user = User(username=username)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get_user(self, username):
        """Retrieves a user by username.

        Args:
            username: String for username.

        Returns:
            User object or None.
        """
        return self._session.query(User).filter(User.username == username).first()
