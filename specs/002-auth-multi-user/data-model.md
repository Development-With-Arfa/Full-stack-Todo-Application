# Data Model: Authentication and Multi-User Task Isolation

**Feature**: 002-auth-multi-user
**Date**: 2026-02-07
**Status**: Design Complete

## Overview

This document defines the data model for user authentication and multi-user task isolation. The model extends the existing task system with user accounts and enforces strict ownership relationships.

---

## Entity Definitions

### 1. User Entity

**Purpose**: Represents a registered user account with authentication credentials.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `email` | String(255) | UNIQUE, NOT NULL, INDEX | User's email address (used for sign-in) |
| `hashed_password` | String(255) | NOT NULL | Bcrypt-hashed password (never store plain text) |
| `created_at` | DateTime | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `updated_at` | DateTime | NOT NULL, DEFAULT NOW() | Last account update timestamp |
| `is_active` | Boolean | NOT NULL, DEFAULT TRUE | Account status (for soft deletion/suspension) |

**Indexes**:
- Primary key on `id`
- Unique index on `email`

**Validation Rules**:
- Email must match regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Password must be at least 8 characters
- Password must contain at least one letter and one number
- Email is case-insensitive (normalize to lowercase before storage)

**SQLModel Definition**:
```python
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import EmailStr

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255, sa_column_kwargs={"nullable": False})
    hashed_password: str = Field(max_length=255, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
    is_active: bool = Field(default=True, sa_column_kwargs={"nullable": False})

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="owner", cascade_delete=True)
```

---

### 2. Task Entity (Updated)

**Purpose**: Represents a todo item owned by a specific user.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| `title` | String(255) | NOT NULL | Task title/summary |
| `description` | Text | NULLABLE | Detailed task description |
| `completed` | Boolean | NOT NULL, DEFAULT FALSE | Task completion status |
| `created_at` | DateTime | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| `updated_at` | DateTime | NOT NULL, DEFAULT NOW() | Last task update timestamp |
| `user_id` | Integer | FOREIGN KEY(users.id), NOT NULL, INDEX | Owner of this task |

**Indexes**:
- Primary key on `id`
- Foreign key index on `user_id`
- Composite index on `(user_id, created_at)` for efficient user task queries

**Validation Rules**:
- Title must not be empty (min 1 character, max 255)
- Description is optional (max 10,000 characters)
- user_id must reference an existing user
- All queries MUST filter by authenticated user_id

**SQLModel Definition**:
```python
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, sa_column_kwargs={"nullable": False})
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})

    # Foreign key to users table
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        sa_column_kwargs={"nullable": False}
    )

    # Relationship to user
    owner: Optional["User"] = Relationship(back_populates="tasks")
```

---

### 3. Authentication Token (Transient)

**Purpose**: JWT token issued by Better Auth for API authentication.

**Note**: This is NOT stored in the database. It's a transient credential issued by Better Auth and verified by the backend.

**Token Structure**:

| Claim | Type | Description |
|-------|------|-------------|
| `sub` | String | Subject - User ID (primary identifier) |
| `email` | String | User's email address |
| `iss` | String | Issuer - Better Auth URL (e.g., "http://localhost:3000") |
| `aud` | String | Audience - Better Auth URL (e.g., "http://localhost:3000") |
| `exp` | Integer | Expiration timestamp (Unix epoch) |
| `iat` | Integer | Issued at timestamp (Unix epoch) |

**Validation Requirements**:
- Signature must be valid (verified using JWKS public key)
- Token must not be expired (`exp` > current time)
- Issuer must match expected value
- Audience must match expected value
- Subject (`sub`) must be present and valid

**Pydantic Model**:
```python
from pydantic import BaseModel
from typing import Optional

class TokenPayload(BaseModel):
    sub: str  # User ID
    email: Optional[str] = None
    iss: str  # Issuer
    aud: str  # Audience
    exp: int  # Expiration
    iat: int  # Issued at
```

---

## Relationships

### User → Task (One-to-Many)

**Relationship**: One user owns zero or more tasks.

**Cardinality**: 1:N

**Foreign Key**: `tasks.user_id` → `users.id`

**Cascade Behavior**:
- **ON DELETE CASCADE**: When a user is deleted, all their tasks are automatically deleted
- **ON UPDATE CASCADE**: If user.id changes (unlikely with auto-increment), task.user_id updates automatically

**SQLModel Relationship**:
```python
# In User model
tasks: list["Task"] = Relationship(back_populates="owner", cascade_delete=True)

# In Task model
owner: Optional["User"] = Relationship(back_populates="tasks")
```

**Query Examples**:
```python
# Get all tasks for a user
user = session.get(User, user_id)
user_tasks = user.tasks

# Get task owner
task = session.get(Task, task_id)
task_owner = task.owner

# Filter tasks by user (recommended for API queries)
tasks = session.exec(
    select(Task).where(Task.user_id == authenticated_user_id)
).all()
```

---

## Database Schema (PostgreSQL)

### SQL DDL

```sql
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);

-- Update tasks table (add user_id foreign key)
ALTER TABLE tasks
ADD COLUMN user_id INTEGER NOT NULL;

ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user_id
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Data Access Patterns

### 1. User Registration

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(email: str, password: str) -> User:
    # Validate email and password
    if not is_valid_email(email):
        raise ValueError("Invalid email format")
    if not is_strong_password(password):
        raise ValueError("Password must be at least 8 characters with letter and number")

    # Check for duplicate email
    existing = session.exec(select(User).where(User.email == email.lower())).first()
    if existing:
        raise ValueError("Email already registered")

    # Hash password and create user
    hashed = pwd_context.hash(password)
    user = User(email=email.lower(), hashed_password=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```

### 2. User Authentication

```python
def authenticate_user(email: str, password: str) -> Optional[User]:
    user = session.exec(
        select(User).where(User.email == email.lower(), User.is_active == True)
    ).first()

    if not user:
        return None

    if not pwd_context.verify(password, user.hashed_password):
        return None

    return user
```

### 3. Task Creation (with Ownership)

```python
def create_task(user_id: int, title: str, description: Optional[str] = None) -> Task:
    task = Task(
        title=title,
        description=description,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### 4. Task Retrieval (Filtered by User)

```python
def get_user_tasks(user_id: int) -> list[Task]:
    """Get all tasks for a specific user."""
    return session.exec(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    ).all()

def get_task_with_ownership_check(task_id: int, user_id: int) -> Optional[Task]:
    """Get a task only if it belongs to the specified user."""
    return session.exec(
        select(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
    ).first()
```

### 5. Task Update (with Ownership Verification)

```python
def update_task(task_id: int, user_id: int, updates: dict) -> Task:
    task = session.get(Task, task_id)

    if not task:
        raise ValueError("Task not found")

    if task.user_id != user_id:
        raise PermissionError("Not authorized to update this task")

    for key, value in updates.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### 6. Task Deletion (with Ownership Verification)

```python
def delete_task(task_id: int, user_id: int) -> None:
    task = session.get(Task, task_id)

    if not task:
        raise ValueError("Task not found")

    if task.user_id != user_id:
        raise PermissionError("Not authorized to delete this task")

    session.delete(task)
    session.commit()
```

---

## Migration Strategy

### Alembic Migration

**File**: `alembic/versions/002_add_user_authentication.py`

```python
"""Add user authentication and task ownership

Revision ID: 002
Revises: 001
Create Date: 2026-02-07
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'])

    # Add user_id to tasks table
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=True))

    # If there are existing tasks, create a default user and assign ownership
    # (Skip this if tasks table is empty)

    # Make user_id non-nullable
    op.alter_column('tasks', 'user_id', nullable=False)

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_tasks_user_id',
        'tasks', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    )

    # Add indexes
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_user_created', 'tasks', ['user_id', 'created_at'])

def downgrade():
    op.drop_index('idx_tasks_user_created', 'tasks')
    op.drop_index('idx_tasks_user_id', 'tasks')
    op.drop_constraint('fk_tasks_user_id', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'user_id')
    op.drop_index('idx_users_email', 'users')
    op.drop_table('users')
```

---

## Security Considerations

### 1. Password Storage
- **NEVER** store plain text passwords
- Use bcrypt with appropriate cost factor (12-14 rounds)
- Salt is automatically handled by bcrypt

### 2. Email Normalization
- Convert all emails to lowercase before storage
- Prevents duplicate accounts with case variations (user@example.com vs USER@example.com)

### 3. User ID from Token
- **ALWAYS** extract user_id from verified JWT token
- **NEVER** accept user_id from request body or URL parameters
- Token signature guarantees authenticity

### 4. Query Filtering
- **ALL** task queries MUST include `WHERE user_id = <authenticated_user_id>`
- Use parameterized queries to prevent SQL injection
- Never construct SQL with string concatenation

### 5. Soft Deletion
- Use `is_active` flag for soft deletion instead of hard deletion
- Allows account recovery and audit trails
- Hard deletion should be a separate admin operation

---

## Performance Considerations

### 1. Indexes
- Primary key on `users.id` (automatic)
- Unique index on `users.email` (for fast login lookups)
- Index on `tasks.user_id` (for fast user task queries)
- Composite index on `(user_id, created_at)` (for sorted user task lists)

### 2. Query Optimization
- Use `select()` with explicit columns instead of `SELECT *`
- Limit result sets with pagination
- Use eager loading for relationships when needed

### 3. Connection Pooling
- Configure SQLModel/SQLAlchemy connection pool
- Recommended: pool_size=20, max_overflow=10 for production

---

## Testing Data

### Sample Users

```python
# Test User A
user_a = User(
    email="alice@example.com",
    hashed_password="$2b$12$...",  # "password123"
    is_active=True
)

# Test User B
user_b = User(
    email="bob@example.com",
    hashed_password="$2b$12$...",  # "password456"
    is_active=True
)
```

### Sample Tasks

```python
# Alice's tasks
task_a1 = Task(title="Alice's Task 1", user_id=1, completed=False)
task_a2 = Task(title="Alice's Task 2", user_id=1, completed=True)

# Bob's tasks
task_b1 = Task(title="Bob's Task 1", user_id=2, completed=False)
```

---

## Validation Checklist

- [x] User entity defined with all required fields
- [x] Task entity updated with user_id foreign key
- [x] Relationships defined (User 1:N Task)
- [x] Cascade delete configured
- [x] Indexes defined for performance
- [x] Validation rules documented
- [x] Security considerations addressed
- [x] Migration strategy defined
- [x] Query patterns documented
- [x] Testing data provided
