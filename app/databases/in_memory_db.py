import json
import os

class InMemoryDatabase:
    """ 
        This "database" works with local json files stored in /data-jsons.
        This db should later be retired when the neo4j operations are fully functional. 
    """
    def __init__(self):
        self.sue_file_path = os.path.join(os.path.dirname(__file__), "../data-jsons/nodes_complete.json")
        self.sue_data = {}
        
        self.load_json()

    def load_json(self):
        """Load JSON from file into memory"""
        try:
            with open(self.sue_file_path, "r", encoding="utf-8") as f:
                self.sue_data = json.load(f)
        except Exception as e:
            print(f"❌Error loading JSON: {e}")
            self.sue_data = {}  # Default empty store if file fails to load

    def get_sue_data(self):
        """Return in-memory JSON data for SUE"""
        return self.sue_data

# Initialize the database when imported
db = InMemoryDatabase()