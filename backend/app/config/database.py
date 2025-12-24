from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import get_settings
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    get_settings().DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=get_settings().DEBUG  # Set to True for SQL query logging in debug mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

logger.info(f"Database engine created with URL: {get_settings().DATABASE_URL.replace(get_settings().DATABASE_URL.split(':')[-1], '***') if get_settings().DATABASE_URL else 'None'}")


def get_db():
    """
    Dependency function to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()