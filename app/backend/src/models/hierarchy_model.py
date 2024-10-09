from pydantic import BaseModel
from typing import List, Optional

class HierarchyItem(BaseModel):
    name: str
    description: str
    parent: str
    
class Hierarchy(BaseModel):
    data: List[HierarchyItem]
    