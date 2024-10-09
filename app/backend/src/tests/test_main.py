import pytest
from fastapi.testclient import TestClient
from app.backend.src.main import app, repository
from app.backend.src.models.hierarchy_model import HierarchyItem

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Clear the database before each test
    repository.db.clear_database()
    yield
    # Teardown: Clear the database after each test
    repository.db.clear_database()

def test_get_data_empty():
    response = client.get("/get-data")
    assert response.status_code == 200
    assert response.json() == {"data": []}

def test_add_item():
    item = {
        "name": "E",
        "description": "This is a description of E",
        "parent": "A"
    }
    response = client.post("/add-item", json=item)
    assert response.status_code == 200
    assert response.json() == {"message": "Item added successfully"}

    # Verify the item was added
    response = client.get("/get-data")
    assert response.status_code == 200
    data = response.json()["data"]
    assert any(i["name"] == "E" for i in data)

def test_get_data_with_initial_data():
    # Add initial data
    for item in [
        {"name": "A", "description": "This is a description of A", "parent": ""},
        {"name": "B", "description": "This is a description of B", "parent": "A"},
        {"name": "C", "description": "This is a description of C", "parent": "A"},
        {"name": "D", "description": "This is a description of D", "parent": "A"},
        {"name": "B-1", "description": "This is a description of B-1", "parent": "B"},
        {"name": "B-2", "description": "This is a description of B-2", "parent": "B"},
        {"name": "B-3", "description": "This is a description of B-3", "parent": "B"}
    ]:
        repository.add_item(HierarchyItem(**item))

    response = client.get("/get-data")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 7
    assert any(i["name"] == "A" for i in data)
    assert any(i["name"] == "B" for i in data)
    assert any(i["name"] == "C" for i in data)
    assert any(i["name"] == "D" for i in data)
    assert any(i["name"] == "B-1" for i in data)
    assert any(i["name"] == "B-2" for i in data)
    assert any(i["name"] == "B-3" for i in data)