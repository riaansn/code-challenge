import pytest
from pydantic import ValidationError
from ..models.hierarchy_model import HierarchyItem, Hierarchy

def test_hierarchy_item_creation():
    item = HierarchyItem(name="Item1", description="This is item 1", parent="Root")
    assert item.name == "Item1"
    assert item.description == "This is item 1"
    assert item.parent == "Root"

def test_hierarchy_item_missing_name():
    with pytest.raises(ValidationError):
        HierarchyItem(description="This is item 1", parent="Root")

def test_hierarchy_item_missing_description():
    with pytest.raises(ValidationError):
        HierarchyItem(name="Item1", parent="Root")

def test_hierarchy_item_missing_parent():
    with pytest.raises(ValidationError):
        HierarchyItem(name="Item1", description="This is item 1")

def test_hierarchy_creation():
    items = [
        HierarchyItem(name="Item1", description="This is item 1", parent="Root"),
        HierarchyItem(name="Item2", description="This is item 2", parent="Item1")
    ]
    hierarchy = Hierarchy(data=items)
    assert len(hierarchy.data) == 2
    assert hierarchy.data[0].name == "Item1"
    assert hierarchy.data[1].parent == "Item1"

def test_hierarchy_empty_data():
    hierarchy = Hierarchy(data=[])
    assert hierarchy.data == []

def test_hierarchy_invalid_data():
    with pytest.raises(ValidationError):
        Hierarchy(data=["invalid data"])