from neo4j import GraphDatabase
import logging as log

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self._driver.close()
        
    def get_hierarchy_data(self):
        with self._driver.session() as session:
            result = session.run("""
                MATCH (n)
                OPTIONAL MATCH (n)-[r:CHILD_OF]->(p)
                RETURN n, p
            """)
            return self._parse_hierarchy(result)
        
    def add_hierarchy_item(self, name, description, parent):
        with self._driver.session() as session:
            if parent:
                session.write_transaction(self._create_node, name, description, parent)
            else:
                session.write_transaction(self._create_root_node, name, description, parent)
                
    @staticmethod
    def _create_node(tx, name, description, parent):
        tx.run("MERGE (p:item {name: $parent}) "
               "CREATE (n:item {name: $name, description: $description, parent: $parent}) "
               "MERGE (n)-[:CHILD_OF]->(p)",
               name=name, description=description, parent=parent)
        
    @staticmethod
    def _create_root_node(tx, name, description, parent):
        tx.run("CREATE (n:item {name: $name, description: $description, parent: $parent})",
               name=name, description=description, parent=parent)
        
    def _parse_hierarchy(self, result):
        hierarchy = []
        for record in result:
            node = record["n"]
            parent = record["p"]
            hierarchy.append({
                "name": node["name"], 
                "description": node["description"],
                "parent": parent["name"] if parent else ""
            })
        return hierarchy