# Data Model: Responsive Task Dashboard

**Feature**: 003-task-dashboard
**Date**: 2026-02-08
**Status**: Complete

## Overview

This document defines the data structures, state management, and data flow for the task dashboard feature. Since this is a frontend-only feature, the focus is on client-side state management and TypeScript interfaces.

## Backend Data Model (Existing)

The backend data model is already established in Feature 002. No changes required.

### Task Entity (Database)

```typescript
interface Task {
  id: number                    // Primary key
  title: string                 // Required, max 255 chars
  description: string | null    // Optional, max 1000 chars
  completed: boolean            // Default: false
  user_id: number              // Foreign key to users table
  created_at: string           // ISO 8601 timestamp
  updated_at: string           // ISO 8601 timestamp
}
```

**Constraints**:
- `id`: Auto-incrementing integer
- `title`: NOT NULL, max length 255
- `description`: Nullable, max length 1000
- `completed`: NOT NULL, default false
- `user_id`: NOT NULL, foreign key with cascade delete
- `created_at`: NOT NULL, auto-set on creation
- `updated_at`: NOT NULL, auto-updated on modification

**Relationships**:
- Task belongs to User (many-to-one)
- User has many Tasks (one-to-many)

## Frontend Data Model

### TypeScript Interfaces

```typescript
// lib/types.ts

// Core Task interface (matches backend)
export interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
  user_id: number
  created_at: string
  updated_at: string
}

// Task creation payload (subset of Task)
export interface TaskCreate {
  title: string
  description?: string
}

// Task update payload (partial Task)
export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}

// Component prop interfaces
export interface TaskCardProps {
  task: Task
  onToggle: (id: number) => Promise<void>
  onEdit: (id: number, data: TaskUpdate) => Promise<void>
  onDelete: (id: number) => Promise<void>
  isEditing: boolean
  onEditModeChange: (editing: boolean) => void
}

export interface TaskFormProps {
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>
  initialData?: Partial<Task>
  loading: boolean
  onCancel?: () => void
  mode: 'create' | 'edit'
}

export interface TaskListProps {
  tasks: Task[]
  loading: boolean
  onToggle: (id: number) => Promise<void>
  onEdit: (id: number, data: TaskUpdate) => Promise<void>
  onDelete: (id: number) => Promise<void>
  editingTaskId: number | null
  onEditingChange: (id: number | null) => void
}

export interface EmptyStateProps {
  message: string
  actionText?: string
  onAction?: () => void
}

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}
```

## State Management

### Page-Level State (TasksPage)

The dashboard page maintains the following state:

```typescript
// app/tasks/page.tsx

interface TasksPageState {
  // Data state
  tasks: Task[]                    // List of user's tasks

  // UI state
  loading: boolean                 // Initial load indicator
  error: string                    // Error message to display

  // Form state
  isCreating: boolean             // Create form submission in progress
  editingTaskId: number | null    // ID of task being edited (null = none)

  // Operation state
  operationInProgress: Set<number> // Track operations per task (toggle, delete)
}

// Initial state
const initialState: TasksPageState = {
  tasks: [],
  loading: true,
  error: "",
  isCreating: false,
  editingTaskId: null,
  operationInProgress: new Set()
}
```

### State Transitions

```
Initial Load:
  loading: true → fetch tasks → loading: false, tasks: [...]

Create Task:
  isCreating: false → submit → isCreating: true → success → isCreating: false, tasks: [...new]

Toggle Completion:
  operationInProgress: {} → toggle → operationInProgress: {id} → success → operationInProgress: {}
  (optimistic update: immediately update task.completed)

Edit Task:
  editingTaskId: null → click edit → editingTaskId: id → submit → editingTaskId: null, tasks: [...updated]

Delete Task:
  operationInProgress: {} → delete → operationInProgress: {id} → success → operationInProgress: {}, tasks: [...filtered]

Error Handling:
  error: "" → operation fails → error: "message" → user dismisses → error: ""
```

### Component-Level State

**TaskForm Component**:
```typescript
interface TaskFormState {
  title: string
  description: string
  errors: {
    title?: string
    description?: string
  }
}
```

**TaskCard Component**:
```typescript
interface TaskCardState {
  // No local state - all state managed by parent
  // Props drive display and behavior
}
```

## Data Flow

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    TasksPage (Smart Component)          │
│                                                          │
│  State:                                                  │
│  - tasks: Task[]                                         │
│  - loading, error, isCreating, editingTaskId            │
│                                                          │
│  Operations:                                             │
│  - loadTasks()                                           │
│  - handleCreateTask(data)                                │
│  - handleToggleComplete(id)                              │
│  - handleEditTask(id, data)                              │
│  - handleDeleteTask(id)                                  │
│                                                          │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ Props (data + callbacks)
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│  TaskForm    │        │  TaskList    │
│              │        │              │
│ Props:       │        │ Props:       │
│ - onSubmit   │        │ - tasks      │
│ - loading    │        │ - onToggle   │
│ - mode       │        │ - onEdit     │
│              │        │ - onDelete   │
└──────────────┘        └──────┬───────┘
                               │
                               │ Props (per task)
                               │
                               ▼
                        ┌──────────────┐
                        │  TaskCard    │
                        │              │
                        │ Props:       │
                        │ - task       │
                        │ - onToggle   │
                        │ - onEdit     │
                        │ - onDelete   │
                        │ - isEditing  │
                        └──────────────┘
```

### Data Flow Patterns

**1. Initial Load**:
```
User navigates to /tasks
  → TasksPage mounts
  → useEffect triggers loadTasks()
  → authenticatedFetch GET /api/v1/tasks
  → Backend returns Task[]
  → setTasks(data)
  → TaskList renders with tasks
  → TaskCard renders for each task
```

**2. Create Task**:
```
User fills TaskForm
  → User clicks "Add Task"
  → TaskForm validates input
  → TaskForm calls onSubmit(data)
  → TasksPage.handleCreateTask(data)
  → setIsCreating(true)
  → authenticatedFetch POST /api/v1/tasks
  → Backend returns new Task
  → setTasks([newTask, ...tasks])
  → setIsCreating(false)
  → TaskForm clears
```

**3. Toggle Completion (Optimistic Update)**:
```
User clicks checkbox
  → TaskCard calls onToggle(id)
  → TasksPage.handleToggleComplete(id)
  → Optimistically update: setTasks(tasks.map(t => t.id === id ? {...t, completed: !t.completed} : t))
  → authenticatedFetch PUT /api/v1/tasks/{id}
  → If success: keep optimistic update
  → If error: rollback + show error
```

**4. Edit Task**:
```
User clicks "Edit"
  → TaskCard calls onEditModeChange(true)
  → TasksPage sets editingTaskId = id
  → TaskCard switches to edit mode (shows TaskForm)
  → User modifies and submits
  → TaskForm calls onSubmit(data)
  → TaskCard calls onEdit(id, data)
  → TasksPage.handleEditTask(id, data)
  → authenticatedFetch PUT /api/v1/tasks/{id}
  → Backend returns updated Task
  → setTasks(tasks.map(t => t.id === id ? updatedTask : t))
  → setEditingTaskId(null)
```

**5. Delete Task**:
```
User clicks "Delete"
  → Browser shows confirm dialog
  → User confirms
  → TaskCard calls onDelete(id)
  → TasksPage.handleDeleteTask(id)
  → authenticatedFetch DELETE /api/v1/tasks/{id}
  → Backend returns 204 No Content
  → setTasks(tasks.filter(t => t.id !== id))
```

## Validation Rules

### Client-Side Validation

**Task Creation/Edit**:
```typescript
function validateTask(data: TaskCreate | TaskUpdate): ValidationResult {
  const errors: Record<string, string> = {}

  // Title validation
  if ('title' in data) {
    if (!data.title || !data.title.trim()) {
      errors.title = "Title is required"
    } else if (data.title.length > 255) {
      errors.title = "Title must be 255 characters or less"
    }
  }

  // Description validation
  if (data.description && data.description.length > 1000) {
    errors.description = "Description must be 1000 characters or less"
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors
  }
}
```

### Server-Side Validation (Existing)

Backend validates:
- Title: required, max 255 chars
- Description: optional, max 1000 chars
- User ownership: task belongs to authenticated user
- Task existence: task ID exists in database

## Error Handling

### Error Types

```typescript
type ErrorType =
  | 'validation'      // Client-side validation failed
  | 'authentication'  // 401 - token invalid/expired
  | 'authorization'   // 403 - user doesn't own resource
  | 'not_found'       // 404 - task doesn't exist
  | 'server'          // 500 - server error
  | 'network'         // Network/fetch error

interface ErrorState {
  type: ErrorType
  message: string
  retryable: boolean
}
```

### Error Handling Strategy

```typescript
async function handleOperation<T>(
  operation: () => Promise<T>,
  errorContext: string
): Promise<T | null> {
  try {
    return await operation()
  } catch (error: any) {
    // Parse error response
    const status = error.status || 0

    if (status === 401) {
      // Authentication error - redirect to sign-in
      router.push('/auth/signin')
      return null
    }

    if (status === 403) {
      setError("You don't have permission to perform this action")
      return null
    }

    if (status === 404) {
      setError("Task not found. It may have been deleted.")
      return null
    }

    // Generic error
    setError(error.message || `Failed to ${errorContext}. Please try again.`)
    return null
  }
}
```

## Performance Considerations

### Optimistic Updates

For better perceived performance, update UI immediately before API call:

```typescript
// Toggle completion - optimistic
const handleToggleComplete = async (id: number) => {
  // Save original state for rollback
  const originalTasks = [...tasks]

  // Optimistic update
  setTasks(tasks.map(t =>
    t.id === id ? {...t, completed: !t.completed} : t
  ))

  try {
    await updateTask(id, { completed: !task.completed })
  } catch (error) {
    // Rollback on error
    setTasks(originalTasks)
    setError("Failed to update task")
  }
}
```

### List Rendering

For large task lists (100+ items):
- Use `key={task.id}` for efficient React reconciliation
- Consider virtualization if performance issues arise (not in initial scope)
- Avoid unnecessary re-renders with proper state management

## Data Persistence

### Local Storage

**Not used** - All data persists to backend immediately. No offline mode or local caching.

### Session Storage

**Not used** - Authentication state managed by Better Auth (HTTP-only cookies).

### Backend Persistence

All task data persists to Neon PostgreSQL via FastAPI endpoints:
- Create: POST /api/v1/tasks
- Read: GET /api/v1/tasks
- Update: PUT /api/v1/tasks/{id}
- Delete: DELETE /api/v1/tasks/{id}

## State Management Summary

| State | Location | Persistence | Updates |
|-------|----------|-------------|---------|
| tasks | TasksPage | Backend | After each mutation |
| loading | TasksPage | Memory | During async operations |
| error | TasksPage | Memory | On operation failure |
| isCreating | TasksPage | Memory | During task creation |
| editingTaskId | TasksPage | Memory | When editing task |
| form values | TaskForm | Memory | User input |
| authentication | Better Auth | HTTP-only cookie | On sign-in/out |

---

**Data Model Status**: ✅ Complete
**All Interfaces Defined**: Yes
**State Management Documented**: Yes
**Ready for Contracts**: Yes
