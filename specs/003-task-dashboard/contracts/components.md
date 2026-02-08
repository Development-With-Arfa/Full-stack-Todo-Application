# Component Contracts: Task Dashboard

**Feature**: 003-task-dashboard
**Date**: 2026-02-08
**Status**: Complete

## Overview

This document defines the interface contracts for all React components in the task dashboard feature. These contracts ensure consistent component APIs and facilitate independent development and testing.

## Component Hierarchy

```
TasksPage (app/tasks/page.tsx)
├── TaskForm (components/TaskForm.tsx) - Create mode
├── TaskList (components/TaskList.tsx)
│   └── TaskCard (components/TaskCard.tsx)
│       └── TaskForm (components/TaskForm.tsx) - Edit mode
├── EmptyState (components/EmptyState.tsx)
└── LoadingSpinner (components/LoadingSpinner.tsx)
```

## Component Contracts

### TasksPage (Smart Component)

**File**: `frontend/app/tasks/page.tsx`

**Purpose**: Main dashboard page that manages all state and orchestrates child components.

**Props**: None (page component)

**State**:
```typescript
interface TasksPageState {
  tasks: Task[]
  loading: boolean
  error: string
  isCreating: boolean
  editingTaskId: number | null
}
```

**Responsibilities**:
- Fetch tasks on mount
- Handle authentication guard (redirect if not authenticated)
- Manage all CRUD operations
- Coordinate state between child components
- Handle errors and display error messages

**Lifecycle**:
```typescript
useEffect(() => {
  // Check authentication
  // Fetch tasks
}, [])
```

---

### TaskForm Component

**File**: `frontend/components/TaskForm.tsx`

**Purpose**: Reusable form for creating and editing tasks.

**Props**:
```typescript
interface TaskFormProps {
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>
  initialData?: Partial<Task>
  loading: boolean
  onCancel?: () => void
  mode: 'create' | 'edit'
}
```

**Prop Descriptions**:
- `onSubmit`: Callback when form is submitted with valid data
- `initialData`: Pre-populate form fields (for edit mode)
- `loading`: Disable form during submission
- `onCancel`: Callback when user cancels edit (optional, only for edit mode)
- `mode`: Determines form behavior and button labels

**State**:
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

**Validation Rules**:
- Title: Required, max 255 characters
- Description: Optional, max 1000 characters

**Behavior**:
- **Create Mode**: Empty form, "Add Task" button, no cancel button
- **Edit Mode**: Pre-filled form, "Save" button, "Cancel" button
- Clear form after successful submission (create mode only)
- Show validation errors inline
- Disable submit button when loading

**Example Usage**:
```typescript
// Create mode
<TaskForm
  mode="create"
  onSubmit={handleCreateTask}
  loading={isCreating}
/>

// Edit mode
<TaskForm
  mode="edit"
  initialData={{ title: task.title, description: task.description }}
  onSubmit={(data) => handleEditTask(task.id, data)}
  onCancel={() => setEditingTaskId(null)}
  loading={false}
/>
```

---

### TaskList Component

**File**: `frontend/components/TaskList.tsx`

**Purpose**: Container component that renders list of tasks or empty state.

**Props**:
```typescript
interface TaskListProps {
  tasks: Task[]
  loading: boolean
  onToggle: (id: number) => Promise<void>
  onEdit: (id: number, data: TaskUpdate) => Promise<void>
  onDelete: (id: number) => Promise<void>
  editingTaskId: number | null
  onEditingChange: (id: number | null) => void
}
```

**Prop Descriptions**:
- `tasks`: Array of tasks to display
- `loading`: Show loading spinner when true
- `onToggle`: Callback to toggle task completion
- `onEdit`: Callback to save edited task
- `onDelete`: Callback to delete task
- `editingTaskId`: ID of task currently being edited (null if none)
- `onEditingChange`: Callback to change editing state

**Behavior**:
- Show LoadingSpinner when loading is true
- Show EmptyState when tasks array is empty and not loading
- Render TaskCard for each task
- Pass callbacks and editing state to TaskCard components

**Responsive Layout**:
- Mobile (< 768px): Stacked layout
- Tablet (768px - 1023px): 2-column grid
- Desktop (1024px+): 3-column grid

**Example Usage**:
```typescript
<TaskList
  tasks={tasks}
  loading={loading}
  onToggle={handleToggleComplete}
  onEdit={handleEditTask}
  onDelete={handleDeleteTask}
  editingTaskId={editingTaskId}
  onEditingChange={setEditingTaskId}
/>
```

---

### TaskCard Component

**File**: `frontend/components/TaskCard.tsx`

**Purpose**: Display individual task with actions (toggle, edit, delete).

**Props**:
```typescript
interface TaskCardProps {
  task: Task
  onToggle: (id: number) => Promise<void>
  onEdit: (id: number, data: TaskUpdate) => Promise<void>
  onDelete: (id: number) => Promise<void>
  isEditing: boolean
  onEditModeChange: (editing: boolean) => void
}
```

**Prop Descriptions**:
- `task`: Task data to display
- `onToggle`: Callback to toggle completion
- `onEdit`: Callback to save edits
- `onDelete`: Callback to delete task
- `isEditing`: Whether this task is in edit mode
- `onEditModeChange`: Callback to enter/exit edit mode

**Display Modes**:

**1. Display Mode** (isEditing = false):
- Show checkbox for completion toggle
- Show task title (with strikethrough if completed)
- Show task description (if present)
- Show creation date
- Show "Edit" button
- Show "Delete" button

**2. Edit Mode** (isEditing = true):
- Show TaskForm with current task data
- Hide display elements
- TaskForm handles save/cancel

**Behavior**:
- Clicking checkbox calls onToggle(task.id)
- Clicking "Edit" calls onEditModeChange(true)
- Clicking "Delete" shows confirmation dialog, then calls onDelete(task.id)
- Completed tasks show with strikethrough and muted color

**Accessibility**:
- Checkbox has aria-label
- Edit/Delete buttons have aria-label
- Keyboard navigation supported

**Example Usage**:
```typescript
<TaskCard
  task={task}
  onToggle={handleToggleComplete}
  onEdit={handleEditTask}
  onDelete={handleDeleteTask}
  isEditing={editingTaskId === task.id}
  onEditModeChange={(editing) => setEditingTaskId(editing ? task.id : null)}
/>
```

---

### EmptyState Component

**File**: `frontend/components/EmptyState.tsx`

**Purpose**: Display message when no tasks exist.

**Props**:
```typescript
interface EmptyStateProps {
  message: string
  actionText?: string
  onAction?: () => void
}
```

**Prop Descriptions**:
- `message`: Main message to display
- `actionText`: Optional button text
- `onAction`: Optional button click handler

**Behavior**:
- Display centered message
- Optionally show action button
- Use friendly, encouraging tone

**Example Usage**:
```typescript
<EmptyState
  message="No tasks yet. Create your first task above!"
/>
```

---

### LoadingSpinner Component

**File**: `frontend/components/LoadingSpinner.tsx`

**Purpose**: Reusable loading indicator.

**Props**:
```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}
```

**Prop Descriptions**:
- `size`: Spinner size (default: 'md')
- `className`: Additional Tailwind classes

**Sizes**:
- `sm`: 16px (h-4 w-4)
- `md`: 32px (h-8 w-8)
- `lg`: 48px (h-12 w-12)

**Behavior**:
- Animated spinning circle
- Blue color (matches brand)
- Accessible (aria-label)

**Example Usage**:
```typescript
<LoadingSpinner size="md" />
```

---

## Component Communication Patterns

### Parent-to-Child (Props)

Data and callbacks flow down from TasksPage to child components:

```
TasksPage
  ├─ tasks → TaskList → TaskCard
  ├─ onToggle → TaskList → TaskCard
  ├─ onEdit → TaskList → TaskCard
  └─ onDelete → TaskList → TaskCard
```

### Child-to-Parent (Callbacks)

Events bubble up through callbacks:

```
TaskCard (user clicks delete)
  → calls onDelete(id)
  → TaskList passes through
  → TasksPage.handleDeleteTask(id)
  → API call + state update
```

### Sibling Communication

Siblings communicate through shared parent state:

```
TaskForm (create mode) submits
  → TasksPage.handleCreateTask()
  → updates tasks state
  → TaskList re-renders with new task
  → TaskCard renders for new task
```

## Testing Contracts

### Unit Testing

Each component should be testable in isolation:

```typescript
// TaskCard.test.tsx
describe('TaskCard', () => {
  it('displays task title and description', () => {
    const task = { id: 1, title: 'Test', description: 'Desc', completed: false }
    render(<TaskCard task={task} onToggle={jest.fn()} ... />)
    expect(screen.getByText('Test')).toBeInTheDocument()
  })

  it('calls onToggle when checkbox clicked', () => {
    const onToggle = jest.fn()
    render(<TaskCard task={task} onToggle={onToggle} ... />)
    fireEvent.click(screen.getByRole('checkbox'))
    expect(onToggle).toHaveBeenCalledWith(task.id)
  })
})
```

### Integration Testing

Test component interactions:

```typescript
// TasksPage.test.tsx
describe('TasksPage', () => {
  it('creates task and displays in list', async () => {
    render(<TasksPage />)
    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'New Task' } })
    fireEvent.click(screen.getByText('Add Task'))
    await waitFor(() => {
      expect(screen.getByText('New Task')).toBeInTheDocument()
    })
  })
})
```

## Error Handling Contracts

### Error Display

Components should handle errors consistently:

```typescript
// Error state in TasksPage
{error && (
  <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
    <p className="text-sm text-red-800">{error}</p>
    <button onClick={() => setError("")} className="text-red-600 underline">
      Dismiss
    </button>
  </div>
)}
```

### Loading States

Components should show loading indicators:

```typescript
// Loading state in TaskForm
<button disabled={loading} className="...">
  {loading ? <LoadingSpinner size="sm" /> : 'Save'}
</button>
```

## Accessibility Contracts

All components must meet WCAG 2.1 Level AA:

### Keyboard Navigation
- All interactive elements focusable
- Tab order logical
- Enter/Space trigger actions

### Screen Readers
- Semantic HTML elements
- ARIA labels for icon buttons
- Status announcements for dynamic content

### Visual
- Color contrast ≥ 4.5:1
- Focus indicators visible
- Text resizable to 200%

---

**Component Contracts Status**: ✅ Complete
**All Interfaces Defined**: Yes
**Communication Patterns Documented**: Yes
**Ready for Implementation**: Yes
