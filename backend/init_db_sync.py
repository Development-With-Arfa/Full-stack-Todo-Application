"""
Synchronous database initialization script for testing.
"""
from sqlmodel import SQLModel, create_engine
from src.models.task import Task
import os
from dotenv import load_dotenv

load_dotenv()

# Use synchronous SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
# Convert async URL to sync URL if needed
if DATABASE_URL.startswith("sqlite+aiosqlite"):
    DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")

print(f"Initializing database with URL: {DATABASE_URL}")

# Create sync engine
sync_engine = create_engine(DATABASE_URL)

def create_db_and_tables_sync():
    """Create database tables synchronously."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(sync_engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables_sync()
    print("Database initialization completed!")