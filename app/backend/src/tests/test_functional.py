import pytest
import os
from fastapi.testclient import TestClient
from ..repositories.repository import HierarchyRepository
from ..repositories.neo4j_database import Neo4jDatabase
from ..main import app

client = TestClient(app)

# Use test database credentials
test_db_uri = os.getenv("TEST_NEO4J_URI", "bolt://localhost:7687")
test_db_user = os.getenv("TEST_NEO4J_USER", "neo4j")
test_db_password = os.getenv("TEST_NEO4J_PASSWORD", "test_password")

# Initialize the test database and repository
test_db = Neo4jDatabase(test_db_uri, test_db_user, test_db_password)
repository = HierarchyRepository(test_db)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Clear the test database before each test
    repository.db.clear_database()
    yield
    # Teardown: Clear the test database after each test
    repository.db.clear_database()

def test_add_and_get_item():
    item = {
        "name": "F",
        "description": "This is a description of F",
        "parent": "A"
    }
    response = client.post("/add-item", json=item)
    assert response.status_code == 200
    assert response.json() == {"message": "Item added successfully"}

    response = client.get("/get-data")
    assert response.status_code == 200
    data = response.json()["data"]
    assert any(i["name"] == "F" for i in data)

def test_update_item():
    item = {
        "name": "G",
        "description": "This is a description of G",
        "parent": "A"
    }
    client.post("/add-item", json=item)

    updated_item = {
        "name": "G",
        "description": "Updated description of G",
        "parent": "A"
    }
    response = client.put("/update-item", json=updated_item)
    assert response.status_code == 200
    assert response.json() == {"message": "Item updated successfully"}

    response = client.get("/get-data")
    assert response.status_code == 200
    data = response.json()["data"]
    assert any(i["description"] == "Updated description of G" for i in data)

def test_delete_item():
    item = {
        "name": "H",
        "description": "This is a description of H",
        "parent": "A"
    }
    client.post("/add-item", json=item)

    response = client.delete("/delete-item", json={"name": "H"})
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

    response = client.get("/get-data")
    assert response.status_code == 200
    data = response.json()["data"]
    assert not any(i["name"] == "H" for i in data)

def test_get_item_by_name():
    item = {
        "name": "I",
        "description": "This is a description of I",
        "parent": "A"
    }
    client.post("/add-item", json=item)

    response = client.get("/get-item/I")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "I"
    assert data["description"] == "This is a description of I"
    assert data["parent"] == "A"