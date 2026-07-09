import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

MYSQL_USER = os.getenv("SQL_USER", "root")
MYSQL_PASSWORD = os.getenv("SQL_PASSWORD", "123456")
MYSQL_HOST = os.getenv("SQL_HOST", "localhost")
MYSQL_PORT = os.getenv("SQL_PORT", "3306")
MYSQL_DB = os.getenv("SQL_DB", "boarding_slots")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
