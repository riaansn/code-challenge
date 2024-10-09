import os
import logging as log
from dotenv import load_dotenv

load_dotenv()

class Config:    
    # Get Neo4j connection details from environment variables
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    ENV = os.getenv("ENV", "production")
    
    @staticmethod
    def configure_logging():
        log_level = log.DEBUG if Config.ENV == "development" else log.INFO
        log.basicConfig(level=log_level)
        
config = Config()
config.configure_logging()
