from persistence.session import SessionLocal
from persistence.models.user import User


class UserRepository:
    """Handles database operations for User entities.

    Attributes:
        session: SQLAlchemy session instance.
    """

    def __init__(self):
        """Initializes a UserRepository with a new database session."""
        self.session = SessionLocal()

    def create_user(self, username):
        """Creates a new user.

        Args:
            username: str

        Returns:
            User
        """
        user = User(username=username)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user(self, username):
        """Retrieves a user by username.

        Args:
            username: str

        Returns:
            User or None
        """
        return self.session.query(User).filter(User.username == username).first()
