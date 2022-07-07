from app.core.settings import API_KEY_NAME, API_KEY, DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base_class import Base
from app.endpoints.base import get_db


engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False,
                                   bind = engine)

Base.metadata.create_all(bind = engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependecy_overrides[get_db] = override_get_db


def get_valid_api_key():
    return {API_KEY_NAME: API_KEY}


def get_invalid_api_key():
    return {API_KEY_NAME: "fake-api-key"}
