// API Response Types

export interface User {
  id: number
  email: string
  name?: string
  created_at: string
  updated_at: string
  is_active: boolean
}

export interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
  created_at: string
  updated_at: string
  user_id: number
}

export interface TaskCreate {
  title: string
  description?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}

// Authentication Types
export interface AuthSession {
  user: User
  session: {
    id: string
    userId: number
    expiresAt: string
  }
}

export interface JWTToken {
  token: string
  expiresAt: string
}

// API Error Types
export interface APIError {
  detail: string
  status?: number
}

export class AuthenticationError extends Error {
  constructor(message: string = "Authentication required") {
    super(message)
    this.name = "AuthenticationError"
  }
}

export class AuthorizationError extends Error {
  constructor(message: string = "You don't have permission to access this resource") {
    super(message)
    this.name = "AuthorizationError"
  }
}

export class ValidationError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "ValidationError"
  }
}

// Component Prop Types

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
