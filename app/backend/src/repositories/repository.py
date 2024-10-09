from ..models.hierarchy_model import HierarchyItem
from .neo4j_database import Neo4jDatabase
from typing import List
import logging as log

class HierarchyRepository:
    
    def __init__(self, db: Neo4jDatabase):
        self.db = db
        
    def get_hierarchy(self) -> List[HierarchyItem]:
        query_result = self.db.get_hierarchy_data()
        return [HierarchyItem(**item) for item in query_result]
    
    def add_item(self, item: HierarchyItem):
        self.db.add_hierarchy_item(item.name, item.description, item.parent)