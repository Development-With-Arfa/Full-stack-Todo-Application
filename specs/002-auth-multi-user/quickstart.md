# Quickstart Guide: Authentication and Multi-User Task Isolation

**Feature**: 002-auth-multi-user
**Date**: 2026-02-07
**Audience**: Developers implementing this feature

## Overview

This guide walks you through setting up Better Auth JWT authentication in the Next.js frontend and implementing JWT verification with user isolation in the FastAPI backend.

**Estimated Setup Time**: 30-45 minutes

---

## Prerequisites

- Node.js 18+ and npm/pnpm installed
- Python 3.11+ and pip installed
- Neon PostgreSQL database configured
- Git repository cloned
- Basic familiarity with Next.js and FastAPI

---

## Part 1: Backend Setup (FastAPI)

### Step 1: Install Dependencies

```bash
cd backend

# Install JWT verification library
pip install pyjwt[crypto]

# Install password hashing library
pip install passlib[bcrypt]

# Update requirements.txt
pip freeze > requirements.txt
```

### Step 2: Configure Environment Variables

Create or update `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database

# Better Auth JWT Configuration
BETTER_AUTH_JWKS_URL=http://localhost:3000/api/auth/jwks
BETTER_AUTH_ISSUER=http://localhost:3000
BETTER_AUTH_AUDIENCE=http://localhost:3000

# CORS
FRONTEND_URL=http://localhost:3000
```

### Step 3: Create Security Module

Create `backend/app/core/security.py`:

```python
import os
from typing import Optional
import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, status
from pydantic import BaseModel

# Configuration from environment
JWKS_URL = os.getenv("BETTER_AUTH_JWKS_URL", "http://localhost:3000/api/auth/jwks")
ISSUER = os.getenv("BETTER_AUTH_ISSUER", "http://localhost:3000")
AUDIENCE = os.getenv("BETTER_AUTH_AUDIENCE", "http://localhost:3000")
ALGORITHM = "EdDSA"  # Better Auth default

# Initialize JWKS client (caches keys automatically)
jwks_client = PyJWKClient(JWKS_URL)

class TokenPayload(BaseModel):
    sub: str  # User ID
    email: Optional[str] = None
    exp: int
    iss: str
    aud: str

def verify_jwt_token(token: str) -> TokenPayload:
    """Verify JWT token using JWKS endpoint."""
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": True,
                "require": ["exp", "iss", "aud", "sub"]
            }
        )
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### Step 4: Create Auth Dependency

Create `backend/app/api/deps.py`:

```python
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_jwt_token, TokenPayload

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenPayload:
    """Extract and verify JWT token from Authorization header."""
    token = credentials.credentials
    return verify_jwt_token(token)

# Type alias for cleaner route signatures
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]
```

### Step 5: Create User Model

Create `backend/app/models/user.py`:

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="owner", cascade_delete=True)
```

### Step 6: Update Task Model

Update `backend/app/models/task.py`:

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to users table
    user_id: int = Field(foreign_key="users.id", index=True)

    # Relationship to user
    owner: Optional["User"] = Relationship(back_populates="tasks")
```

### Step 7: Run Database Migration

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add user authentication and task ownership"

# Review the generated migration file in alembic/versions/

# Run migration
alembic upgrade head
```

### Step 8: Update Task Routes

Update `backend/app/routes/tasks.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.api.deps import CurrentUser
from app.models.task import Task
from app.db import get_session

router = APIRouter()

@router.get("/tasks")
async def list_tasks(
    current_user: CurrentUser,
    session: Session = Depends(get_session)
) -> list[Task]:
    """List all tasks for authenticated user."""
    user_id = int(current_user.sub)
    tasks = session.exec(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    ).all()
    return tasks

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser,
    session: Session = Depends(get_session)
) -> Task:
    """Create a new task for authenticated user."""
    user_id = int(current_user.sub)
    task = Task(**task_data.dict(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/tasks/{task_id}")
async def get_task(
    task_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session)
) -> Task:
    """Get a specific task (ownership verified)."""
    user_id = int(current_user.sub)
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return task

@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: CurrentUser,
    session: Session = Depends(get_session)
) -> Task:
    """Update a task (ownership verified)."""
    user_id = int(current_user.sub)
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session)
):
    """Delete a task (ownership verified)."""
    user_id = int(current_user.sub)
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    session.delete(task)
    session.commit()
```

### Step 9: Update CORS Configuration

Update `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Part 2: Frontend Setup (Next.js)

### Step 1: Install Dependencies

```bash
cd frontend

# Install Better Auth
npm install better-auth

# Install Better Auth CLI (for migrations)
npm install -D @better-auth/cli
```

### Step 2: Configure Environment Variables

Create or update `frontend/.env.local`:

```bash
# Better Auth Configuration
BETTER_AUTH_SECRET=<generate-with-openssl-rand-base64-32>
BETTER_AUTH_URL=http://localhost:3000

# Database (same as backend)
DATABASE_URL=postgresql://user:password@host/database

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Generate BETTER_AUTH_SECRET**:
```bash
openssl rand -base64 32
```

### Step 3: Configure Better Auth

Create `frontend/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt({
      jwt: {
        expirationTime: "24h",
        issuer: process.env.BETTER_AUTH_URL!,
        audience: process.env.BETTER_AUTH_URL!,
      }
    })
  ],
})
```

### Step 4: Create Auth API Route

Create `frontend/app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from "@/lib/auth"

export const { GET, POST } = auth.handler
```

### Step 5: Run Database Migration

```bash
# Generate Better Auth tables (users, sessions, jwks, etc.)
npx @better-auth/cli migrate
```

### Step 6: Create Auth Client

Create `frontend/lib/auth-client.ts`:

```typescript
import { createAuthClient } from "better-auth/react"
import { jwtClient } from "better-auth/client/plugins"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  plugins: [jwtClient()],
})
```

### Step 7: Create API Client with JWT

Create `frontend/lib/api-client.ts`:

```typescript
import { authClient } from "./auth-client"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function authenticatedFetch(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  // Get JWT token from Better Auth
  const { data } = await authClient.token()

  if (!data?.token) {
    throw new Error("Not authenticated")
  }

  // Attach token to Authorization header
  const headers = new Headers(options.headers)
  headers.set("Authorization", `Bearer ${data.token}`)
  headers.set("Content-Type", "application/json")

  return fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  })
}

// Helper functions
export async function getTasks() {
  const response = await authenticatedFetch("/api/tasks")
  if (!response.ok) throw new Error("Failed to fetch tasks")
  return response.json()
}

export async function createTask(title: string, description?: string) {
  const response = await authenticatedFetch("/api/tasks", {
    method: "POST",
    body: JSON.stringify({ title, description }),
  })
  if (!response.ok) throw new Error("Failed to create task")
  return response.json()
}
```

### Step 8: Create Sign-Up Page

Create `frontend/app/auth/signup/page.tsx`:

```typescript
"use client"

import { useState } from "react"
import { authClient } from "@/lib/auth-client"
import { useRouter } from "next/navigation"

export default function SignUpPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    try {
      await authClient.signUp.email({
        email,
        password,
        name,
      })
      router.push("/tasks")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign up failed")
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8 p-6 border rounded-lg">
      <h1 className="text-2xl font-bold mb-4">Sign Up</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div>
          <label className="block mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div>
          <label className="block mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border rounded px-3 py-2"
            minLength={8}
            required
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Sign Up
        </button>
      </form>
    </div>
  )
}
```

### Step 9: Create Sign-In Page

Create `frontend/app/auth/signin/page.tsx`:

```typescript
"use client"

import { useState } from "react"
import { authClient } from "@/lib/auth-client"
import { useRouter } from "next/navigation"

export default function SignInPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    try {
      await authClient.signIn.email({
        email,
        password,
      })
      router.push("/tasks")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign in failed")
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8 p-6 border rounded-lg">
      <h1 className="text-2xl font-bold mb-4">Sign In</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div>
          <label className="block mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Sign In
        </button>
      </form>
    </div>
  )
}
```

---

## Part 3: Testing

### Test Backend JWT Verification

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Test with curl (replace TOKEN with actual JWT from Better Auth)
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/api/tasks
```

### Test Frontend Authentication

```bash
# Start frontend
cd frontend
npm run dev

# Open browser
# 1. Go to http://localhost:3000/auth/signup
# 2. Create an account
# 3. Go to http://localhost:3000/tasks
# 4. Create a task
# 5. Open DevTools Network tab and verify Authorization header
```

### Test Multi-User Isolation

1. Sign up as User A, create tasks
2. Sign out
3. Sign up as User B
4. Verify User B cannot see User A's tasks
5. Try to access User A's task by ID (should get 403 Forbidden)

---

## Troubleshooting

### Issue: "JWKS endpoint not reachable"

**Solution**: Ensure Next.js frontend is running on port 3000 and `/api/auth/jwks` endpoint is accessible.

```bash
curl http://localhost:3000/api/auth/jwks
```

### Issue: "Token has expired"

**Solution**: Get a fresh token by signing in again. Tokens expire after 24 hours by default.

### Issue: "CORS error"

**Solution**: Verify CORS configuration in FastAPI allows `http://localhost:3000` and includes credentials.

### Issue: "Foreign key constraint violation"

**Solution**: Ensure users table exists before creating tasks. Run migrations in correct order.

---

## Next Steps

After completing this quickstart:

1. Run `/sp.tasks` to generate detailed implementation tasks
2. Implement comprehensive test suite
3. Add error handling and validation
4. Deploy to staging environment
5. Conduct security audit

---

## Reference Links

- [Better Auth Documentation](https://www.better-auth.com/docs)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
