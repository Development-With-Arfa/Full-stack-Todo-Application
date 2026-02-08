---
name: backend-skill
description: Backend development skill for building REST routes, handling requests/responses, and connecting APIs to databases. Use when implementing server-side logic.
---

# Backend Skill — Routes, APIs & Database Connection

## Instructions
Build backend systems with these requirements:

### 1. REST API Route Generation
- Create clean RESTful endpoints (GET, POST, PUT, DELETE)
- Follow consistent route naming and structure
- Separate public and protected routes

### 2. Request & Response Handling
- Validate incoming requests using schemas (Pydantic, Zod, etc.)
- Return correct HTTP status codes and error messages
- Ensure predictable response formats

### 3. Authentication & Access Control
- Protect sensitive endpoints with JWT/session middleware
- Enforce user ownership for all multi-user resources
- Reject unauthorized or invalid requests

### 4. Database Integration
- Connect backend routes to PostgreSQL/Neon reliably
- Use ORM or SQL queries safely (avoid SQL injection)
- Handle transactions and persistence correctly

### 5. Backend Architecture Best Practices
- Organize code into routes, services, and data layers
- Maintain scalable, readable, production-ready structure
- Log errors safely without leaking sensitive data

## Example Snippet (FastAPI Route + DB Access)
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Task

router = APIRouter()

@router.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
