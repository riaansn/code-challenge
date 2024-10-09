from fastapi import FastAPI, Depends
from .repositories.repository import HierarchyRepository
from .models.hierarchy_model import HierarchyItem
from .repositories.neo4j_database import Neo4jDatabase
from .config.config import Config
import time
from neo4j.exceptions import ServiceUnavailable

app = FastAPI()
config = Config()

# Initialize the Neo4j database using configuration settings
db = Neo4jDatabase(config.NEO4J_URI, config.NEO4J_USER, config.NEO4J_PASSWORD)
repository = HierarchyRepository(db)

# Initial data to be added if the database is empty
initial_data = [
    {"name": "A", "description": "This is a description of A", "parent": ""},
    {"name": "B", "description": "This is a description of B", "parent": "A"},
    {"name": "C", "description": "This is a description of C", "parent": "A"},
    {"name": "D", "description": "This is a description of D", "parent": "A"},
    {"name": "B-1", "description": "This is a description of B-1", "parent": "B"},
    {"name": "B-2", "description": "This is a description of B-2", "parent": "B"},
    {"name": "B-3", "description": "This is a description of B-3", "parent": "B"}
]

@app.on_event("startup")
async def startup_event():
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            # Check if the database is empty
            if not db.get_hierarchy_data():
                # Add initial data to the database
                for item in initial_data:
                    name = item["name"]
                    description = item["description"]
                    parent = item.get("parent")
                    db.add_hierarchy_item(name, description, parent)
            break  # Exit the loop if successful
        except ServiceUnavailable:
            if attempt < max_retries - 1:
                print(f"Neo4j is not available, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Neo4j is not available.")
                raise

@app.get("/get-data")
async def get_data(repo: HierarchyRepository = Depends(lambda: repository)):
    data = repo.get_hierarchy()
    return {"data": data}

@app.post("/add-item")
async def add_item(item: HierarchyItem, repo: HierarchyRepository = Depends(lambda: repository)):
    repo.add_item(item)
    return {"message": "Item added successfully"}

@app.on_event("shutdown")
async def shutdown_event():
    await db.close()
