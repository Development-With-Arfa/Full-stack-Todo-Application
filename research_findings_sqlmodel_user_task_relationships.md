# SQLModel Database Patterns: User-Task Relationships Research

## Executive Summary

Research completed on SQLModel foreign key patterns, relationship definitions, and migration strategies for implementing a user-task relationship in the Todo App backend.

**Current Database State:**
- PostgreSQL database with existing `tasks` table
- `user_id` column already exists (VARCHAR, NOT NULL)
- No foreign key constraints currently defined
- Table is empty (0 rows) - migration will be straightforward
- Alembic installed but not initialized

---

## 1. SQLModel Foreign Key Patterns and Syntax

### 1.1 Basic Foreign Key Definition

Foreign keys in SQLModel are defined using the `Field()` function with the `foreign_key` parameter:

```python
from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import UUID

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    user_id: str = Field(max_length=255, foreign_key="users.id")
```

**Key Points:**
- Format: `foreign_key="table_name.column_name"`
- The foreign key references the target table's primary key or unique column
- Column type must match the referenced column type

### 1.2 Complete User-Task Relationship Models

Here's the complete implementation with bidirectional relationships:

```python
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship


# User Model
class User(SQLModel, table=True):
    """User model representing a user in the database."""
    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=255)
    email: str = Field(unique=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: One user has many tasks
    tasks: List["Task"] = Relationship(
        back_populates="user",
        cascade_delete=True  # Python-level cascade
    )


# Task Model (Updated)
class Task(SQLModel, table=True):
    """Task model representing a task in the database."""
    __tablename__ = "tasks"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, nullable=False)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key with cascade delete
    user_id: str = Field(
        max_length=255,
        foreign_key="users.id",
        ondelete="CASCADE"  # Database-level cascade
    )

    # Relationship: Many tasks belong to one user
    user: Optional[User] = Relationship(back_populates="tasks")
```

### 1.3 Relationship Attributes Explained

**`back_populates`**: Creates bidirectional relationship synchronization
- On `User.tasks`: points to `"user"` (the attribute name in Task model)
- On `Task.user`: points to `"tasks"` (the attribute name in User model)
- Keeps both sides synchronized in memory before committing

**`Relationship()` characteristics:**
- Does NOT create a database column
- Provides convenient object access: `task.user.email` or `user.tasks[0].title`
- Automatically loads related objects when accessed (lazy loading by default)

---

## 2. Cascading Delete Behavior

### 2.1 Two-Level Cascade Configuration

**Best Practice: Configure BOTH levels** for robust cascade behavior:

```python
# Database-level: ondelete parameter on Field
user_id: str = Field(
    max_length=255,
    foreign_key="users.id",
    ondelete="CASCADE"  # Database handles deletion
)

# Python-level: cascade_delete parameter on Relationship
tasks: List["Task"] = Relationship(
    back_populates="user",
    cascade_delete=True  # SQLAlchemy handles deletion
)
```

### 2.2 Why Both Levels?

1. **Database-level (`ondelete="CASCADE"`):**
   - Protects against direct SQL manipulation
   - Works even when bypassing the ORM
   - Enforced by the database engine
   - More efficient for bulk operations

2. **Python-level (`cascade_delete=True`):**
   - Manages in-memory Python objects
   - Triggers ORM events and hooks
   - Ensures consistency before commit
   - Required when database doesn't support foreign keys (e.g., SQLite without PRAGMA)

### 2.3 Cascade Options

**CASCADE**: Automatically delete child records when parent is deleted
```python
user_id: str = Field(foreign_key="users.id", ondelete="CASCADE")
```

**SET NULL**: Set foreign key to NULL when parent is deleted (requires nullable column)
```python
user_id: Optional[str] = Field(default=None, foreign_key="users.id", ondelete="SET NULL")
```

**RESTRICT**: Prevent parent deletion if children exist
```python
user_id: str = Field(foreign_key="users.id", ondelete="RESTRICT")
```

**For this project**: Use `CASCADE` since tasks should be deleted when a user is deleted.

---

## 3. Migration Strategy for Adding user_id Foreign Key

### 3.1 Current Situation Analysis

**Database State:**
- Table: `tasks` exists with `user_id` column (VARCHAR, NOT NULL)
- No foreign key constraint currently defined
- No data in table (0 rows)
- No User table exists yet

**Migration Requirements:**
1. Create `users` table
2. Add foreign key constraint to existing `tasks.user_id` column
3. No data migration needed (table is empty)

### 3.2 Alembic Setup (Not Yet Initialized)

**Step 1: Initialize Alembic**
```bash
cd backend
alembic init alembic
```

This creates:
- `alembic.ini` - configuration file
- `alembic/` directory with `env.py`, `script.py.mako`, and `versions/`

**Step 2: Configure alembic.ini**
```ini
# alembic.ini
sqlalchemy.url = postgresql+asyncpg://user:pass@host/db?sslmode=require

# Or use environment variable (recommended)
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Step 3: Configure env.py for SQLModel**
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# Import all models so Alembic can detect them
from src.models.task import Task
from src.models.user import User  # When created

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 3.3 Migration Script Example

**Create migration:**
```bash
alembic revision -m "create users table and add foreign key to tasks"
```

**Migration file (alembic/versions/xxxx_create_users_and_fk.py):**
```python
"""create users table and add foreign key to tasks

Revision ID: xxxx
Revises:
Create Date: 2026-02-07
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'xxxx'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Add foreign key constraint to tasks.user_id
    # Since table is empty, no data migration needed
    op.create_foreign_key(
        'fk_tasks_user_id_users',  # constraint name
        'tasks',                    # source table
        'users',                    # referent table
        ['user_id'],                # local columns
        ['id'],                     # remote columns
        ondelete='CASCADE'          # cascade delete behavior
    )


def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint('fk_tasks_user_id_users', 'tasks', type_='foreignkey')

    # Drop users table
    op.drop_table('users')
```

**Run migration:**
```bash
alembic upgrade head
```

### 3.4 Alternative: Using SQLModel.metadata.create_all()

If not using Alembic, update `src/database/engine.py`:

```python
async def create_db_and_tables():
    """Create database tables synchronously to avoid greenlet issues."""

    # Import ALL models so SQLModel registers them
    from src.models.task import Task
    from src.models.user import User  # Add this import

    print("Creating tables...")
    SQLModel.metadata.create_all(sync_engine)
    print("Tables created successfully!")
```

**Note:** This approach:
- Creates tables if they don't exist
- Does NOT modify existing tables
- Does NOT add foreign keys to existing columns
- Requires manual SQL for schema changes

---

## 4. Handling Existing Data During Migration

### 4.1 Current Project Status

**Good News:** The `tasks` table is empty (0 rows), so no data migration is needed.

### 4.2 If Data Existed (For Future Reference)

**Scenario:** Adding foreign key to table with existing data

**Challenge:** Existing `user_id` values must reference valid users

**Solution Approaches:**

**Option 1: Three-Step Migration**
```python
def upgrade() -> None:
    # Step 1: Create users table
    op.create_table('users', ...)

    # Step 2: Populate users table with existing user_ids
    # Get unique user_ids from tasks
    connection = op.get_bind()
    result = connection.execute(
        sa.text("SELECT DISTINCT user_id FROM tasks")
    )
    user_ids = [row[0] for row in result]

    # Insert users (with default email)
    for user_id in user_ids:
        connection.execute(
            sa.text("INSERT INTO users (id, email, created_at) VALUES (:id, :email, NOW())"),
            {"id": user_id, "email": f"{user_id}@placeholder.com"}
        )

    # Step 3: Add foreign key constraint
    op.create_foreign_key(
        'fk_tasks_user_id_users',
        'tasks',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
```

**Option 2: Make Column Nullable First**
```python
def upgrade() -> None:
    # Step 1: Create users table
    op.create_table('users', ...)

    # Step 2: Make user_id nullable temporarily
    op.alter_column('tasks', 'user_id', nullable=True)

    # Step 3: Add foreign key (allows NULL values)
    op.create_foreign_key(
        'fk_tasks_user_id_users',
        'tasks',
        'users',
        ['user_id'],
        ['id'],
        ondelete='SET NULL'
    )

    # Step 4: Clean up orphaned tasks (optional)
    connection = op.get_bind()
    connection.execute(
        sa.text("DELETE FROM tasks WHERE user_id NOT IN (SELECT id FROM users)")
    )
```

**Option 3: Separate Data Migration Script**

Alembic documentation recommends keeping data migrations separate from schema migrations:

1. Run schema migration (add nullable column)
2. Run separate Python script to migrate data
3. Run final schema migration (add constraints, make NOT NULL)

---

## 5. Best Practices Summary

### 5.1 Model Definition Checklist

- ✅ Define foreign key on the "many" side (Task)
- ✅ Use `ondelete="CASCADE"` for database-level cascade
- ✅ Use `Relationship()` on both sides with `back_populates`
- ✅ Add `cascade_delete=True` on the "one" side (User) for Python-level cascade
- ✅ Match data types between foreign key and referenced column
- ✅ Consider nullable vs NOT NULL based on business logic

### 5.2 Migration Checklist

- ✅ Initialize Alembic if not already done
- ✅ Configure env.py to import all SQLModel models
- ✅ Create users table first (referenced table must exist)
- ✅ Add foreign key constraint to tasks table
- ✅ Handle existing data if table is not empty
- ✅ Test both upgrade and downgrade paths
- ✅ Use descriptive constraint names for easier debugging

### 5.3 Testing Checklist

- ✅ Test cascade delete: deleting user deletes all tasks
- ✅ Test foreign key constraint: cannot create task with invalid user_id
- ✅ Test relationship access: `task.user` and `user.tasks` work correctly
- ✅ Test NULL handling if foreign key is nullable
- ✅ Test migration rollback (downgrade)

---

## 6. Code Examples for Common Operations

### 6.1 Creating Related Objects

```python
from sqlmodel import Session

# Create user and tasks together
user = User(id="user123", email="user@example.com")
task1 = Task(title="Task 1", user_id=user.id)
task2 = Task(title="Task 2", user_id=user.id)

session.add(user)
session.add(task1)
session.add(task2)
session.commit()

# Or use relationship
user = User(id="user123", email="user@example.com")
user.tasks = [
    Task(title="Task 1"),
    Task(title="Task 2")
]
session.add(user)
session.commit()
```

### 6.2 Querying with Relationships

```python
from sqlmodel import select

# Get user with all tasks (lazy loading)
statement = select(User).where(User.id == "user123")
user = session.exec(statement).first()
print(user.tasks)  # Automatically loads tasks

# Get task with user
statement = select(Task).where(Task.id == task_id)
task = session.exec(statement).first()
print(task.user.email)  # Automatically loads user

# Eager loading (more efficient)
from sqlalchemy.orm import selectinload

statement = select(User).options(selectinload(User.tasks)).where(User.id == "user123")
user = session.exec(statement).first()
```

### 6.3 Cascade Delete in Action

```python
# Delete user - all tasks automatically deleted
user = session.get(User, "user123")
session.delete(user)
session.commit()
# All tasks with user_id="user123" are now deleted
```

---

## 7. PostgreSQL-Specific Considerations

### 7.1 Current Database

- **Engine:** PostgreSQL (Neon)
- **Driver:** asyncpg (async operations)
- **Foreign Key Support:** Full support, enabled by default

### 7.2 Checking Foreign Keys

```sql
-- View foreign keys on tasks table
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    rc.delete_rule
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_name = 'tasks';
```

### 7.3 Performance Considerations

- Foreign key constraints add overhead on INSERT/UPDATE/DELETE
- Indexes are automatically created on foreign key columns in PostgreSQL
- CASCADE operations can be expensive with large datasets
- Consider using `passive_deletes="all"` for very large tables

---

## 8. Implementation Roadmap

### Phase 1: Model Updates
1. Create `src/models/user.py` with User model
2. Update `src/models/task.py` to add foreign key and relationship
3. Update imports in `src/database/engine.py`

### Phase 2: Migration Setup (Choose One)

**Option A: Alembic (Recommended for Production)**
1. Initialize Alembic: `alembic init alembic`
2. Configure `alembic.ini` with database URL
3. Update `alembic/env.py` for SQLModel
4. Create migration: `alembic revision -m "add users and foreign key"`
5. Write upgrade/downgrade functions
6. Run migration: `alembic upgrade head`

**Option B: SQLModel Direct (Simple, No Migration History)**
1. Update `create_db_and_tables()` to import User model
2. Run application - tables created automatically
3. Manually add foreign key with SQL if needed

### Phase 3: Testing
1. Test user creation
2. Test task creation with valid user_id
3. Test foreign key constraint (invalid user_id should fail)
4. Test cascade delete
5. Update existing tests to handle user context

### Phase 4: Service Layer Updates
1. Update task service to validate user_id exists
2. Add user service for user operations
3. Update API endpoints if needed

---

## 9. References and Sources

- **SQLModel Relationships:** https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/define-relationships-attributes/
- **SQLModel back_populates:** https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/back-populates/
- **SQLModel Cascade Delete:** https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/cascade-delete-relationships/
- **Alembic Tutorial:** https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Alembic Operations:** https://alembic.sqlalchemy.org/en/latest/ops.html
- **SQLAlchemy Foreign Keys:** https://docs.sqlalchemy.org/en/20/core/constraints.html
- **Alembic Cookbook:** https://alembic.sqlalchemy.org/en/latest/cookbook.html

---

## 10. Current Project Files

**Relevant Files:**
- `E:\Todo_App_II\backend\src\models\task.py` - Task model (needs foreign key update)
- `E:\Todo_App_II\backend\src\database\engine.py` - Database engine and table creation
- `E:\Todo_App_II\backend\src\services\task_service.py` - Task service (already uses user_id)
- `E:\Todo_App_II\backend\requirements.txt` - Dependencies (alembic already installed)

**Database:**
- PostgreSQL on Neon
- Table: `tasks` with `user_id` column (VARCHAR, NOT NULL)
- No foreign keys currently defined
- Empty table (0 rows)

**Next Steps:**
1. Create User model
2. Add foreign key constraint to Task model
3. Set up Alembic or use direct SQLModel approach
4. Test the relationship

---

*Research completed: 2026-02-07*
*Database: PostgreSQL (Neon)*
*Framework: SQLModel 0.0.16, SQLAlchemy 2.0.36, Alembic 1.13.1*
