import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from . import Base


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    result = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    played_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
