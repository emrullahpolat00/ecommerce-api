import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app
from sqlalchemy import text

TEST_DB_URL = "sqlite:///./test.db"

engine_test = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def _clean_test_db():
    # Eski test.db varsa sil (Windows kilit sorunlarını azaltır)
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            # Eğer dosya kilitliyse, test sonunda zaten overwrite olur.
            pass

    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            pass


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    # app içindeki get_db dependency’sini test db ile override et
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    
@pytest.fixture(autouse=True)
def _clear_data_between_tests(db_session):
    """
    Her testten önce DB tablolarını temizler.
    UNIQUE hatalarını ve testler arası bağımlılığı engeller.
    """
    # Foreign key ilişkileri nedeniyle silme sırası önemli
    db_session.execute(text("DELETE FROM reviews"))
    db_session.execute(text("DELETE FROM order_items"))
    db_session.execute(text("DELETE FROM orders"))
    db_session.execute(text("DELETE FROM products"))
    db_session.execute(text("DELETE FROM categories"))
    db_session.execute(text("DELETE FROM users"))
    db_session.commit()
    yield