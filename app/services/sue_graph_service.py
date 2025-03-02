from app.databases.in_memory_db import db

def get_sue_data():
    """Return the stored JSON data."""
    return db.get_sue_data()
