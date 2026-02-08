import os
import sys
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def fix_tasks_table():
    """Fix the tasks table schema by changing user_id from INTEGER to VARCHAR(255)."""

    # Convert asyncpg URL to psycopg2 URL
    db_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

    try:
        print("Connecting to database...")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        print("Dropping existing tasks table...")
        cursor.execute("DROP TABLE IF EXISTS tasks CASCADE;")

        print("Creating tasks table with correct schema...")
        cursor.execute("""
            CREATE TABLE tasks (
                id UUID PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description VARCHAR(1000),
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                user_id VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)

        print("Creating index on user_id...")
        cursor.execute("CREATE INDEX idx_tasks_user_id ON tasks(user_id);")

        conn.commit()
        print("✓ Tasks table fixed successfully!")
        print("✓ user_id column is now VARCHAR(255) instead of INTEGER")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"✗ Failed to fix tasks table: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_tasks_table()
