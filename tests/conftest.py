import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from src.core.config import settings
from src.database.session import (
    Base,
    create_all_tables,
    get_db,
    get_engine,
    get_session_local,
)
from src.main import app

from tests.helpers.quiz_api import QuizApiClient


@pytest.fixture(scope="session")
def setup_live_database():
    create_all_tables()

    yield


@pytest.fixture(scope="function")
def db_session(setup_live_database):
    connection = get_engine().connect()
    transaction = connection.begin()

    SessionLocalFactory = get_session_local()
    session = SessionLocalFactory(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def live_client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def quiz_api_client(live_client):
    base_url = f"{settings.ENDPOINT}{settings.API_PREFIX}"
    return QuizApiClient(client=live_client, base_url=base_url)


@pytest.fixture(scope="function")
def lifespan_test_env(mocker):
    from src.database import session

    mocker.patch.object(session, "_engine", None)
    mocker.patch.object(session, "_SessionLocal", None)

    engine = session.get_engine()

    SCHEMA_NAME = "test_lifespan"

    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};"))
        conn.commit()

    isolated_engine = engine.execution_options(schema_translate_map={None: SCHEMA_NAME})
    Base.metadata.schema = SCHEMA_NAME

    mocker.patch("src.database.session.get_engine", return_value=isolated_engine)
    yield isolated_engine

    with engine.connect() as conn:
        conn.execute(text(f"DROP SCHEMA IF EXISTS {SCHEMA_NAME} CASCADE;"))
        conn.commit()

    Base.metadata.schema = None
    engine.dispose()
