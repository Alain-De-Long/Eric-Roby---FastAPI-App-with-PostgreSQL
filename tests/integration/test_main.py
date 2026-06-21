from fastapi.testclient import TestClient
from sqlalchemy import inspect
from src.main import app


def test_app_lifespan_triggers_table_creation(lifespan_test_env):
    with TestClient(app):
        inspector = inspect(lifespan_test_env)
        tables = inspector.get_table_names(schema="test_lifespan")

        assert len(tables) > 0, (
            "Lifespan function fail to initialize any tables under the DB!"
        )
        assert "questions" in tables, (
            "Table 'questions' was not found after lifespan execution!"
        )
        assert "choices" in tables, (
            "Table 'choices' was not found after lifespan execution!"
        )
