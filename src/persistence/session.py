# pylint: skip-file
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.user import User
from .models.game import Game
from .models import Base

DB_PATH = os.getenv("SQLITE_PATH", os.path.join(os.getcwd(), "data", "chess.db"))
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
