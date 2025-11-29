# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

# Create SQLite database
DATABASE_URL = "sqlite:///./ecopickup.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
