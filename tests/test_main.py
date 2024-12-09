from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/recipes")
    assert response.status_code == 200

if __name__ == '__main__':
    test_read_main()
