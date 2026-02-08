---
name: database-skill
description: Database schema design, table creation, migrations, and PostgreSQL best practices. Use when building or maintaining database persistence.
---

# Database Skill — Schema & Migrations

## Instructions
Design and manage database systems with these requirements:

### 1. Table & Schema Design
- Create normalized, scalable table structures
- Define correct relationships (1–1, 1–many, many–many)
- Use proper data types and naming conventions

### 2. Constraints & Integrity
- Apply primary keys, foreign keys, and unique constraints
- Enforce NOT NULL rules where required
- Prevent inconsistent or duplicate data

### 3. Migrations & Version Control
- Manage schema changes using migrations (Alembic or similar)
- Ensure migrations are reversible and consistent
- Never modify production schema manually

### 4. Query & Performance Best Practices
- Write efficient SQL queries
- Add indexes for frequently queried columns
- Avoid N+1 query patterns

### 5. Persistence & Multi-User Isolation
- Ensure data ownership enforcement at the database level
- Prevent cross-user access through correct schema rules
- Maintain reliable backend persistence with PostgreSQL/Neon

## Example Snippet (SQL Table Creation)
```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  title TEXT NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
