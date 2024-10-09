import pytest
from unittest.mock import Mock
from ..repositories.repository import HierarchyRepository
from ..models.hierarchy_model import HierarchyItem

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def repository(mock_db):
    return HierarchyRepository(mock_db)

def test_get_hierarchy(repository, mock_db):
    mock_db.get_hierarchy_data.return_value = [
        {"name": "Item1", "description": "Description1", "parent": None},
        {"name": "Item2", "description": "Description2", "parent": "Item1"}
    ]
    
    result = repository.get_hierarchy()
    
    assert len(result) == 2
    assert result[0].name == "Item1"
    assert result[0].description == "Description1"
    assert result[0].parent is None
    assert result[1].name == "Item2"
    assert result[1].description == "Description2"
    assert result[1].parent == "Item1"
    mock_db.get_hierarchy_data.assert_called_once()

def test_add_item(repository, mock_db):
    item = HierarchyItem(name="Item1", description="Description1", parent=None)
    
    repository.add_item(item)
    
    mock_db.add_hierarchy_item.assert_called_once_with("Item1", "Description1", None)