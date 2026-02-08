# API Integration Contracts: Task Dashboard

**Feature**: 003-task-dashboard
**Date**: 2026-02-08
**Status**: Complete

## Overview

This document defines the API integration contracts between the frontend dashboard and the FastAPI backend. All endpoints are from Feature 002 (existing) - no new backend endpoints required.

## Base Configuration

**Base URL**: `http://localhost:8000` (development)
**Authentication**: JWT Bearer token in Authorization header
**Content-Type**: `application/json`

## Authentication

All API requests must include a valid JWT token:

```typescript
Authorization: Bearer <jwt-token>
```

The `authenticatedFetch` wrapper (from `lib/api-client.ts`) automatically handles this:

```typescript
import { authenticatedFetch } from "@/lib/api-client"

const response = await authenticatedFetch("/api/v1/tasks")
```

## API Endpoints

### 1. Get All Tasks

**Endpoint**: `GET /api/v1/tasks`

**Purpose**: Retrieve all tasks for the authenticated user

**Authentication**: Required

**Request**:
```http
GET /api/v1/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer <jwt-token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive docs for the authentication system",
    "completed": false,
    "user_id": 1,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  },
  {
    "id": 2,
    "title": "Review pull requests",
    "description": null,
    "completed": true,
    "user_id": 1,
    "created_at": "2024-01-02T10:30:00Z",
    "updated_at": "2024-01-02T15:45:00Z"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired JWT token
- `500 Internal Server Error`: Database error

**Frontend Implementation**:
```typescript
async function loadTasks(): Promise<Task[]> {
  const response = await authenticatedFetch("/api/v1/tasks")
  if (!response.ok) {
    throw new Error("Failed to load tasks")
  }
  return await response.json()
}
```

---

### 2. Create Task

**Endpoint**: `POST /api/v1/tasks`

**Purpose**: Create a new task for the authenticated user

**Authentication**: Required

**Request**:
```http
POST /api/v1/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Request Body Schema**:
```typescript
interface TaskCreateRequest {
  title: string        // Required, max 255 chars
  description?: string // Optional, max 1000 chars
}
```

**Response** (201 Created):
```json
{
  "id": 3,
  "title": "New task title",
  "description": "Optional task description",
  "completed": false,
  "user_id": 1,
  "created_at": "2024-01-03T09:00:00Z",
  "updated_at": "2024-01-03T09:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired JWT token
- `422 Unprocessable Entity`: Validation error (empty title, too long)
- `500 Internal Server Error`: Database error

**Frontend Implementation**:
```typescript
async function createTask(data: TaskCreate): Promise<Task> {
  const response = await authenticatedFetch("/api/v1/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Failed to create task")
  }

  return await response.json()
}
```

---

### 3. Update Task

**Endpoint**: `PUT /api/v1/tasks/{id}`

**Purpose**: Update an existing task (title, description, or completion status)

**Authentication**: Required

**Request**:
```http
PUT /api/v1/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

**Request Body Schema**:
```typescript
interface TaskUpdateRequest {
  title?: string       // Optional, max 255 chars
  description?: string // Optional, max 1000 chars
  completed?: boolean  // Optional
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "user_id": 1,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-03T10:15:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired JWT token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task does not exist
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Database error

**Frontend Implementation**:
```typescript
async function updateTask(id: number, data: TaskUpdate): Promise<Task> {
  const response = await authenticatedFetch(`/api/v1/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    if (response.status === 403) {
      throw new Error("You don't have permission to update this task")
    }
    if (response.status === 404) {
      throw new Error("Task not found")
    }
    throw new Error("Failed to update task")
  }

  return await response.json()
}
```

---

### 4. Delete Task

**Endpoint**: `DELETE /api/v1/tasks/{id}`

**Purpose**: Delete a task

**Authentication**: Required

**Request**:
```http
DELETE /api/v1/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer <jwt-token>
```

**Response** (204 No Content):
```
(empty body)
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired JWT token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task does not exist
- `500 Internal Server Error`: Database error

**Frontend Implementation**:
```typescript
async function deleteTask(id: number): Promise<void> {
  const response = await authenticatedFetch(`/api/v1/tasks/${id}`, {
    method: "DELETE"
  })

  if (!response.ok) {
    if (response.status === 403) {
      throw new Error("You don't have permission to delete this task")
    }
    if (response.status === 404) {
      throw new Error("Task not found")
    }
    throw new Error("Failed to delete task")
  }
}
```

---

## API Client Wrapper

### authenticatedFetch Function

**Location**: `frontend/lib/api-client.ts` (existing)

**Purpose**: Wrapper around fetch that automatically includes JWT token

**Signature**:
```typescript
async function authenticatedFetch(
  endpoint: string,
  options?: RequestInit
): Promise<Response>
```

**Behavior**:
1. Retrieves JWT token from Better Auth
2. Adds Authorization header with Bearer token
3. Prepends base URL to endpoint
4. Makes fetch request
5. Returns Response object

**Error Handling**:
- Throws error if token retrieval fails
- Throws error if response status indicates error
- Caller responsible for parsing response

**Usage Example**:
```typescript
import { authenticatedFetch } from "@/lib/api-client"

// GET request
const response = await authenticatedFetch("/api/v1/tasks")
const tasks = await response.json()

// POST request
const response = await authenticatedFetch("/api/v1/tasks", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "New task" })
})
const newTask = await response.json()
```

---

## Error Handling Patterns

### Standard Error Response Format

Backend returns errors in this format:

```json
{
  "detail": "Error message here"
}
```

### Frontend Error Handling

```typescript
async function apiOperation<T>(
  operation: () => Promise<Response>
): Promise<T> {
  try {
    const response = await operation()

    if (!response.ok) {
      // Parse error response
      const error = await response.json().catch(() => ({ detail: "Unknown error" }))

      // Handle specific status codes
      if (response.status === 401) {
        // Redirect to sign-in
        router.push("/auth/signin")
        throw new Error("Authentication required")
      }

      if (response.status === 403) {
        throw new Error("You don't have permission to perform this action")
      }

      if (response.status === 404) {
        throw new Error("Resource not found")
      }

      // Generic error
      throw new Error(error.detail || "Operation failed")
    }

    // Parse success response
    if (response.status === 204) {
      return null as T // No content
    }

    return await response.json()

  } catch (error: any) {
    // Network error or other exception
    if (error.message) {
      throw error
    }
    throw new Error("Network error. Please check your connection.")
  }
}
```

---

## Request/Response Examples

### Complete Task Creation Flow

**1. User submits form**:
```typescript
const formData = {
  title: "Write documentation",
  description: "Complete API docs"
}
```

**2. Frontend validates**:
```typescript
if (!formData.title.trim()) {
  setError("Title is required")
  return
}
```

**3. Frontend makes API call**:
```typescript
const response = await authenticatedFetch("/api/v1/tasks", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(formData)
})
```

**4. Backend validates and creates**:
- Verifies JWT token
- Extracts user_id from token
- Validates title (not empty, max 255 chars)
- Creates task in database with user_id
- Returns created task

**5. Frontend updates UI**:
```typescript
const newTask = await response.json()
setTasks([newTask, ...tasks])
```

### Complete Task Toggle Flow

**1. User clicks checkbox**:
```typescript
const task = tasks.find(t => t.id === 1)
const newCompleted = !task.completed
```

**2. Frontend optimistically updates**:
```typescript
setTasks(tasks.map(t =>
  t.id === 1 ? { ...t, completed: newCompleted } : t
))
```

**3. Frontend makes API call**:
```typescript
const response = await authenticatedFetch("/api/v1/tasks/1", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ completed: newCompleted })
})
```

**4. Backend validates and updates**:
- Verifies JWT token
- Checks task ownership
- Updates task in database
- Returns updated task

**5. Frontend confirms or rolls back**:
```typescript
if (response.ok) {
  // Success - keep optimistic update
} else {
  // Error - rollback
  setTasks(originalTasks)
  setError("Failed to update task")
}
```

---

## Rate Limiting

**Current**: No rate limiting implemented

**Future Consideration**: If rate limiting is added, handle 429 Too Many Requests:

```typescript
if (response.status === 429) {
  const retryAfter = response.headers.get("Retry-After")
  throw new Error(`Too many requests. Please try again in ${retryAfter} seconds.`)
}
```

---

## CORS Configuration

**Backend CORS Settings** (from Feature 002):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Frontend Requirements**:
- Requests must include credentials: `credentials: "include"`
- Already handled by `authenticatedFetch` wrapper

---

## Testing API Integration

### Manual Testing with curl

```bash
# Get JWT token (sign in first via UI, then extract from DevTools)
TOKEN="your-jwt-token-here"

# Get all tasks
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/tasks

# Create task
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test description"}' \
  http://localhost:8000/api/v1/tasks

# Update task
curl -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}' \
  http://localhost:8000/api/v1/tasks/1

# Delete task
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/tasks/1
```

### Testing with Browser DevTools

1. Open DevTools → Network tab
2. Perform action in UI
3. Inspect request/response
4. Verify:
   - Authorization header present
   - Request body correct
   - Response status correct
   - Response body matches expected format

---

## API Contract Summary

| Endpoint | Method | Auth | Request Body | Response | Purpose |
|----------|--------|------|--------------|----------|---------|
| `/api/v1/tasks` | GET | Required | None | Task[] | Get all user tasks |
| `/api/v1/tasks` | POST | Required | TaskCreate | Task | Create new task |
| `/api/v1/tasks/{id}` | PUT | Required | TaskUpdate | Task | Update task |
| `/api/v1/tasks/{id}` | DELETE | Required | None | 204 | Delete task |

**All endpoints**:
- Require JWT authentication
- Enforce user ownership
- Return JSON responses (except DELETE)
- Follow RESTful conventions

---

**API Integration Contracts Status**: ✅ Complete
**All Endpoints Documented**: Yes
**Error Handling Defined**: Yes
**Ready for Implementation**: Yes
