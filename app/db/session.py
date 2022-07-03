from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.configuration import Config

config = Config()

SQLALCHEMY_DATABASE_URI = config.db_url


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    # required for sqlite
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
