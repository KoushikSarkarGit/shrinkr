from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.dependencies import get_settings
from app.main import app


def test_health_check():
    test_settings = Settings(
        app_name="Shrinkr Test",
        app_version="test",
        environment="testing",
        debug=False,
    )

    app.dependency_overrides[get_settings] = lambda: test_settings

    client = TestClient(app)

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "Ok",
        "environment": "testing",
    }

    app.dependency_overrides.clear()
