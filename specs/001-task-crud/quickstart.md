# Quick Start Guide: Task CRUD Backend

## Prerequisites
- Python 3.11+
- pip package manager
- Access to Neon PostgreSQL instance

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi sqlmodel uvicorn pytest python-multipart python-dotenv
```

## Configuration

1. Set up environment variables:
```bash
# Create .env file in project root
DATABASE_URL="postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
```

2. Verify database connection settings

## Running the Application

1. Start the development server:
```bash
uvicorn backend.src.main:app --reload
```

2. The API will be available at: `http://localhost:8000`

3. API documentation available at: `http://localhost:8000/docs`

## Running Tests

1. Execute unit tests:
```bash
pytest tests/unit/
```

2. Execute integration tests:
```bash
pytest tests/integration/
```

3. Run all tests:
```bash
pytest tests/
```

## Sample API Calls

1. Create a task:
```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample task", "description": "Task description"}'
```

2. Get all tasks for a user:
```bash
curl "http://localhost:8000/api/user123/tasks"
```

3. Get a specific task:
```bash
curl "http://localhost:8000/api/user123/tasks/task-id"
```

4. Update a task:
```bash
curl -X PUT "http://localhost:8000/api/user123/tasks/task-id" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated task", "completed": true}'
```

5. Delete a task:
```bash
curl -X DELETE "http://localhost:8000/api/user123/tasks/task-id"
```

## Troubleshooting

- **Database connection issues**: Verify DATABASE_URL in environment variables
- **Port conflicts**: Use `--port 8001` or different port for uvicorn
- **Migration errors**: Run database migrations manually if needed
- **Dependency issues**: Update requirements.txt with exact versions

## Next Steps

- Implement JWT authentication for user validation
- Add comprehensive logging and monitoring
- Deploy to production environment
- Set up automated testing pipeline