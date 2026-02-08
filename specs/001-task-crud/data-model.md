# Data Model: Task CRUD Operations

## Overview
Entity definitions and relationships for the task management system.

## Task Entity

### Fields
- **id** (UUID/Integer, Primary Key, Auto-generated)
  - Unique identifier for each task
  - Required for all operations
  - Auto-generated on creation

- **title** (String, Required, 1-255 characters)
  - Human-readable title of the task
  - Required field with length validation
  - Used for display and search purposes

- **description** (Text, Optional, up to 1000 characters)
  - Additional details about the task
  - Nullable field for extended information
  - Optional for brevity in simple tasks

- **completed** (Boolean, Default: False)
  - Status indicator for task completion
  - Boolean field with false as default
  - Controls visual representation and filtering

- **user_id** (String/UUID, Required, Foreign Key)
  - Reference to the owning user
  - Critical for multi-user isolation
  - Required for all access validation

- **created_at** (DateTime, Default: Current Timestamp)
  - Record of when task was created
  - Immutable after creation
  - Useful for sorting and audit trails

- **updated_at** (DateTime, Default: Current Timestamp)
  - Record of last modification
  - Updated on every change operation
  - Useful for sorting and change tracking

### Constraints
- Title must be between 1-255 characters
- Description optional, up to 1000 characters
- User_id must reference an existing user
- Title cannot be empty/null
- Completed defaults to false on creation

### Indexes
- Primary: id (automatically indexed)
- Secondary: user_id (for efficient user-based queries)
- Composite: (user_id, created_at) for efficient retrieval and sorting

## Relationships

### Task ↔ User
- Many-to-One relationship
- Each task belongs to one user
- Each user can have multiple tasks
- User identity controls access to tasks

## State Transitions

### Creation State
- id: auto-generated
- title: from input (validated)
- description: from input (optional)
- completed: false (default)
- user_id: from request context
- created_at: current timestamp
- updated_at: current timestamp

### Update State
- id: unchanged
- title: from input (if provided and validated)
- description: from input (if provided)
- completed: from input (if provided)
- user_id: unchanged
- created_at: unchanged
- updated_at: updated to current timestamp

### Read States
- All fields returned based on user_id validation
- Different representations for lists vs. individual tasks

## Validation Rules

### Input Validation
- Title: Required, 1-255 chars, trimmed
- Description: Optional, max 1000 chars
- Completed: Boolean only
- User_id: Valid user identifier format

### Business Validation
- User must own the task for access
- Cannot delete non-existent tasks
- Update operations respect ownership