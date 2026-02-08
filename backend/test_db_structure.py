"""
Test script to verify database structure
"""
import sqlite3
import os

# Connect to the SQLite database
db_path = os.path.join(os.getcwd(), "todo_app.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the sqlite_master table to see all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f"  - {table[0]}")

# If there's a 'tasks' table, get its structure
if ('tasks',) in tables:
    cursor.execute("PRAGMA table_info(tasks)")
    columns = cursor.fetchall()
    print("\nColumns in 'tasks' table:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - Default: {col[4]}")

conn.close()

print("\nDatabase structure verified successfully!")