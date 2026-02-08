# Research Findings: Better Auth JWT Integration with FastAPI

**Feature**: 002-auth-multi-user
**Date**: 2026-02-07
**Researcher**: Claude Sonnet 4.5
**Status**: Complete

## Overview

This document consolidates research findings for integrating Better Auth JWT authentication in a Next.js frontend with JWT verification in a FastAPI backend. The research addresses all technical unknowns identified in the implementation plan.

---

## 1. Better Auth JWT Plugin Configuration

### 1.1 Enabling JWT Plugin in Better Auth for Next.js

**Installation**:
```bash
npm install better-auth
```

**Basic Configuration** (`lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  database: {
    // Your database config
  },
  plugins: [
    jwt()
  ]
})
```

**After adding the plugin**, run database migration:
```bash
npx @better-auth/cli migrate
# or
npx @better-auth/cli generate
```

This creates a `jwks` table to store public/private key pairs.

### 1.2 JWT Token Structure and Claims

**Default Payload**: By default, Better Auth includes the entire user object in the JWT payload.

**Custom Payload Configuration**:
```typescript
jwt({
  jwt: {
    definePayload: ({user}) => ({
      id: user.id,
      email: user.email,
      role: user.role
    })
  }
})
```

**Standard JWT Claims Configuration**:
```typescript
jwt({
  jwt: {
    issuer: "https://example.com",           // Default: BASE_URL
    audience: "https://example.com",         // Default: BASE_URL
    expirationTime: "1h",                    // Default: 15 minutes
    getSubject: (session) => session.user.email  // Default: user.id
  }
})
```

**Token Structure**:
- **Header**: Contains algorithm (default: EdDSA with Ed25519) and key ID (`kid`)
- **Payload**: User data + standard claims (iss, aud, exp, sub)
- **Signature**: Cryptographically signed with private key

### 1.3 Shared Secret Configuration

**Important Discovery**: Better Auth JWT plugin uses **asymmetric cryptography** (public/private key pairs) by default, NOT shared secrets.

**Two Verification Approaches**:

#### Approach A: JWKS Endpoint (Recommended)
Better Auth exposes a JWKS endpoint at `/api/auth/jwks` that provides the public key. The backend fetches this public key to verify tokens.

**No shared secret needed** - only the public key is shared, which is safe.

**Configuration**:
- Frontend: Configure Better Auth with JWT plugin (generates key pairs automatically)
- Backend: Use PyJWT's `PyJWKClient` to fetch public keys from JWKS endpoint

#### Approach B: Shared Secret (Alternative)
If you need symmetric signing (HS256), you would need to configure Better Auth differently. However, the documentation primarily focuses on asymmetric algorithms.

**For this project**: Use Approach A (JWKS endpoint) as it's more secure and the recommended pattern.

### 1.4 Environment Variables

**Frontend** (`.env.local`):
```bash
BETTER_AUTH_SECRET=<generated-secret-32-chars>  # For encryption/hashing
BETTER_AUTH_URL=http://localhost:3000           # Base URL
```

**Backend** (`.env`):
```bash
BETTER_AUTH_JWKS_URL=http://localhost:3000/api/auth/jwks
BETTER_AUTH_ISSUER=http://localhost:3000
BETTER_AUTH_AUDIENCE=http://localhost:3000
```

**Generate BETTER_AUTH_SECRET**:
```bash
openssl rand -base64 32
```

### 1.5 Client-Side Token Retrieval

**Method 1: Client Plugin (Recommended)**:
```typescript
import { createAuthClient } from "better-auth/react"
import { jwtClient } from "better-auth/client/plugins"

const authClient = createAuthClient({
  baseURL: "http://localhost:3000",
  plugins: [jwtClient()]
})

// Get JWT token
const { data } = await authClient.token()
const jwtToken = data.token
```

**Method 2: From Response Header**:
```typescript
await authClient.getSession({
  fetchOptions: {
    onSuccess: (ctx) => {
      const jwt = ctx.response.headers.get("set-auth-jwt")
    }
  }
})
```

**Method 3: Direct Endpoint**:
```typescript
await fetch("/api/auth/token", {
  headers: {
    "Authorization": `Bearer ${sessionToken}`
  }
})
```

---

## 2. FastAPI JWT Verification

### 2.1 Best Practices for JWT Verification in FastAPI

**Key Principles**:
1. **Verify signature** - Always validate the JWT signature
2. **Check expiration** - Validate `exp` claim
3. **Validate issuer** - Verify `iss` matches expected value
4. **Validate audience** - Verify `aud` matches your service
5. **Extract user identity** - Get user_id from verified token claims
6. **Use dependency injection** - Make auth reusable across routes

### 2.2 PyJWT vs python-jose Comparison

| Feature | PyJWT | python-jose |
|---------|-------|-------------|
| **Maintenance** | Actively maintained | Less active |
| **JWKS Support** | ✅ Built-in `PyJWKClient` | ⚠️ Manual implementation |
| **Algorithm Support** | Extensive (RS256, ES256, EdDSA) | Good |
| **Documentation** | Excellent | Moderate |
| **Dependencies** | Minimal (cryptography for RSA) | PyCrypto |
| **Performance** | Fast | Fast |
| **Recommendation** | **Use PyJWT** | Legacy projects |

**Decision**: Use **PyJWT** for this project due to built-in JWKS support and better maintenance.

### 2.3 Implementation with PyJWT and JWKS

**Installation**:
```bash
pip install pyjwt[crypto]
```

**Security Module** (`backend/src/core/security.py`):
```python
from typing import Optional
import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, status
from pydantic import BaseModel

# Configuration (from environment)
JWKS_URL = "http://localhost:3000/api/auth/jwks"
ISSUER = "http://localhost:3000"
AUDIENCE = "http://localhost:3000"
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
    """
    Verify JWT token using JWKS endpoint.

    Args:
        token: JWT token string

    Returns:
        TokenPayload with user information

    Raises:
        HTTPException: If token is invalid, expired, or verification fails
    """
    try:
        # Get signing key from JWKS endpoint (cached)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Decode and verify token
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### 2.4 Dependency Injection Pattern for Auth

**Auth Dependency** (`backend/src/api/deps.py`):
```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import verify_jwt_token, TokenPayload

# OAuth2 scheme for automatic OpenAPI documentation
security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenPayload:
    """
    Dependency to extract and verify JWT token from Authorization header.

    Usage:
        @app.get("/protected")
        async def protected_route(
            current_user: Annotated[TokenPayload, Depends(get_current_user)]
        ):
            user_id = current_user.sub
            return {"user_id": user_id}
    """
    token = credentials.credentials
    return verify_jwt_token(token)

# Type alias for cleaner route signatures
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]
```

**Usage in Routes** (`backend/src/api/v1/endpoints/tasks.py`):
```python
from fastapi import APIRouter, Depends
from api.deps import CurrentUser
from models.task import Task
from services.task_service import TaskService

router = APIRouter()

@router.get("/tasks")
async def list_tasks(
    current_user: CurrentUser,
    task_service: TaskService = Depends()
) -> list[Task]:
    """List all tasks for the authenticated user."""
    user_id = current_user.sub
    return await task_service.get_tasks_by_user(user_id)

@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser,
    task_service: TaskService = Depends()
) -> Task:
    """Create a new task for the authenticated user."""
    user_id = current_user.sub
    return await task_service.create_task(user_id, task_data)

@router.get("/tasks/{task_id}")
async def get_task(
    task_id: int,
    current_user: CurrentUser,
    task_service: TaskService = Depends()
) -> Task:
    """Get a specific task (ownership verified)."""
    user_id = current_user.sub
    task = await task_service.get_task(task_id)

    if task.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this task"
        )

    return task
```

---

## 3. User-Task Database Relationship

### 3.1 SQLModel Foreign Key Pattern

**User Model** (`backend/src/models/user.py`):
```python
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
```

**Updated Task Model** (`backend/src/models/task.py`):
```python
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to users table
    user_id: int = Field(foreign_key="users.id", index=True)
```

### 3.2 Migration Strategy

**Option A: Alembic Migration (Recommended)**:
```python
# alembic/versions/xxx_add_user_auth.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Add user_id to tasks table
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=True))

    # Create a default user for existing tasks (if any)
    # Then update existing tasks to reference this user

    # Make user_id non-nullable after data migration
    op.alter_column('tasks', 'user_id', nullable=False)

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_tasks_user_id',
        'tasks', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])

def downgrade():
    op.drop_constraint('fk_tasks_user_id', 'tasks', type_='foreignkey')
    op.drop_index('ix_tasks_user_id', 'tasks')
    op.drop_column('tasks', 'user_id')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
```

**Option B: SQLModel Direct Creation** (for new databases):
```python
from sqlmodel import create_engine, SQLModel
from models.user import User
from models.task import Task

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

### 3.3 Cascading Delete Behavior

**Recommendation**: Use `CASCADE` on delete so that when a user is deleted, all their tasks are automatically deleted.

**SQLModel Configuration**:
```python
class Task(SQLModel, table=True):
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        ondelete="CASCADE"  # Delete tasks when user is deleted
    )
```

**Database-Level Constraint**:
```sql
ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user_id
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;
```

---

## 4. Token Storage and Transmission

### 4.1 HTTP-only Cookies vs localStorage

| Aspect | HTTP-only Cookies | localStorage |
|--------|-------------------|--------------|
| **XSS Protection** | ✅ Immune to XSS | ❌ Vulnerable to XSS |
| **CSRF Protection** | ⚠️ Needs CSRF tokens | ✅ Not vulnerable to CSRF |
| **Automatic Sending** | ✅ Sent automatically | ❌ Manual attachment |
| **Cross-domain** | ⚠️ Requires CORS config | ✅ Easier cross-domain |
| **Size Limit** | 4KB | 5-10MB |
| **Better Auth Default** | ✅ Uses HTTP-only cookies | - |

**Decision**: Use **Better Auth's default (HTTP-only cookies)** for session management. The JWT token is retrieved on-demand for API calls.

### 4.2 CORS Configuration

**Frontend API Client** (`frontend/lib/apiClient.ts`):
```typescript
import { authClient } from './auth'

export async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  // Get JWT token from Better Auth
  const { data } = await authClient.token()

  if (!data?.token) {
    throw new Error('Not authenticated')
  }

  // Attach token to Authorization header
  const headers = new Headers(options.headers)
  headers.set('Authorization', `Bearer ${data.token}`)

  return fetch(url, {
    ...options,
    headers,
    credentials: 'include', // Include cookies for Better Auth session
  })
}
```

**Backend CORS Configuration** (`backend/src/main.py`):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

### 4.3 Token Refresh Strategy

**Better Auth Approach**: Better Auth manages session refresh automatically through its cookie-based session system.

**For Hackathon Scope**: No explicit refresh token implementation needed. Use Better Auth's default session expiry (configurable, typically 24 hours).

**If Needed Later**:
```typescript
jwt({
  jwt: {
    expirationTime: "24h"  // Adjust as needed
  }
})
```

---

## 5. Multi-User Testing Strategy

### 5.1 pytest Fixtures for Multi-User Scenarios

**Test Fixtures** (`backend/tests/conftest.py`):
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from main import app
from models.user import User
from models.task import Task
from core.security import create_access_token

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def user_a(session: Session) -> User:
    """Create test user A."""
    user = User(
        email="user_a@example.com",
        hashed_password="hashed_password_a"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def user_b(session: Session) -> User:
    """Create test user B."""
    user = User(
        email="user_b@example.com",
        hashed_password="hashed_password_b"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def token_user_a(user_a: User) -> str:
    """Generate JWT token for user A."""
    return create_test_token(user_a.id)

@pytest.fixture
def token_user_b(user_b: User) -> str:
    """Generate JWT token for user B."""
    return create_test_token(user_b.id)

def create_test_token(user_id: int) -> str:
    """Helper to create test JWT tokens."""
    return f"Bearer test_token_user_{user_id}"
```

**Multi-User Test Example** (`backend/tests/test_task_isolation.py`):
```python
def test_user_cannot_access_other_user_tasks(
    client: TestClient,
    user_a: User,
    user_b: User,
    token_user_a: str,
    token_user_b: str,
    session: Session
):
    """Test that User B cannot access User A's tasks."""
    # User A creates a task
    task_a = Task(
        title="User A's Task",
        description="Private task",
        user_id=user_a.id
    )
    session.add(task_a)
    session.commit()
    session.refresh(task_a)

    # User B tries to access User A's task
    response = client.get(
        f"/tasks/{task_a.id}",
        headers={"Authorization": token_user_b}
    )

    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]

def test_users_see_only_own_tasks(
    client: TestClient,
    user_a: User,
    user_b: User,
    token_user_a: str,
    token_user_b: str,
    session: Session
):
    """Test that each user sees only their own tasks."""
    # Create tasks for both users
    for i in range(3):
        session.add(Task(title=f"Task A{i}", user_id=user_a.id))
        session.add(Task(title=f"Task B{i}", user_id=user_b.id))
    session.commit()

    # User A lists tasks
    response_a = client.get(
        "/tasks",
        headers={"Authorization": token_user_a}
    )
    tasks_a = response_a.json()
    assert len(tasks_a) == 3
    assert all("Task A" in task["title"] for task in tasks_a)

    # User B lists tasks
    response_b = client.get(
        "/tasks",
        headers={"Authorization": token_user_b}
    )
    tasks_b = response_b.json()
    assert len(tasks_b) == 3
    assert all("Task B" in task["title"] for task in tasks_b)
```

### 5.2 Frontend Testing with Mocked Authentication

**Mock Auth Client** (`frontend/__tests__/mocks/auth.ts`):
```typescript
export const mockAuthClient = {
  token: jest.fn().mockResolvedValue({
    data: { token: 'mock-jwt-token' }
  }),
  getSession: jest.fn().mockResolvedValue({
    data: {
      user: { id: '1', email: 'test@example.com' }
    }
  }),
  signIn: jest.fn(),
  signUp: jest.fn(),
  signOut: jest.fn(),
}
```

### 5.3 End-to-End Testing

**Playwright Multi-User Test** (`e2e/auth.spec.ts`):
```typescript
import { test, expect } from '@playwright/test'

test('multi-user task isolation', async ({ browser }) => {
  // Create two browser contexts (two users)
  const contextA = await browser.newContext()
  const contextB = await browser.newContext()

  const pageA = await contextA.newPage()
  const pageB = await contextB.newPage()

  // User A signs up and creates a task
  await pageA.goto('/auth/signup')
  await pageA.fill('[name="email"]', 'usera@example.com')
  await pageA.fill('[name="password"]', 'password123')
  await pageA.click('button[type="submit"]')

  await pageA.goto('/tasks')
  await pageA.fill('[name="title"]', 'User A Task')
  await pageA.click('button:has-text("Add Task")')

  // User B signs up
  await pageB.goto('/auth/signup')
  await pageB.fill('[name="email"]', 'userb@example.com')
  await pageB.fill('[name="password"]', 'password456')
  await pageB.click('button[type="submit"]')

  // User B should not see User A's task
  await pageB.goto('/tasks')
  const taskCount = await pageB.locator('[data-testid="task-item"]').count()
  expect(taskCount).toBe(0)

  await contextA.close()
  await contextB.close()
})
```

---

## Key Decisions and Recommendations

### 1. Use JWKS Endpoint (Not Shared Secret)
- Better Auth uses asymmetric cryptography by default
- Backend fetches public keys from `/api/auth/jwks`
- More secure than shared secrets
- Supports key rotation

### 2. Use PyJWT Library
- Better JWKS support than python-jose
- Actively maintained
- Excellent documentation
- Built-in caching

### 3. Dependency Injection for Auth
- Use FastAPI's `Depends()` pattern
- Makes auth explicit and testable
- Reusable across all protected routes

### 4. CASCADE Delete for User-Task Relationship
- Automatically clean up tasks when user is deleted
- Maintains referential integrity
- Simplifies user deletion logic

### 5. HTTP-only Cookies for Session
- Use Better Auth's default cookie-based session
- Retrieve JWT on-demand for API calls
- Best security posture against XSS

---

## Implementation Checklist

- [ ] Install PyJWT with crypto support: `pip install pyjwt[crypto]`
- [ ] Configure Better Auth with JWT plugin in Next.js
- [ ] Set up JWKS endpoint URL in backend environment
- [ ] Implement JWT verification with PyJWKClient
- [ ] Create auth dependency for FastAPI routes
- [ ] Add user_id foreign key to tasks table
- [ ] Update all task queries to filter by user_id
- [ ] Implement ownership verification for update/delete
- [ ] Configure CORS for Authorization header
- [ ] Create multi-user test fixtures
- [ ] Write task isolation tests
- [ ] Test token expiration handling

---

## References

- [Better Auth JWT Plugin Documentation](https://www.better-auth.com/docs/plugins/jwt)
- [Better Auth Session Management](https://www.better-auth.com/docs/concepts/session-management)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/en/stable/)
- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Better Auth Installation Guide](https://www.better-auth.com/docs/installation)
