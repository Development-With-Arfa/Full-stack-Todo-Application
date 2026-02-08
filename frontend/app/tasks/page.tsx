"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { authClient } from "@/lib/auth-client"
import { authenticatedFetch } from "@/lib/api-client"
import { Task, TaskCreate, TaskUpdate } from "@/lib/types"
import TaskList from "@/components/TaskList"
import TaskForm from "@/components/TaskForm"

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [isCreating, setIsCreating] = useState(false)
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null)
  const [hasCriticalError, setHasCriticalError] = useState(false)
  const router = useRouter()

  // Authentication guard - check if user is authenticated
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data } = await authClient.getSession()
        if (!data?.session) {
          router.push("/auth/signin")
          return
        }
        // Session is valid, proceed to load tasks
        loadTasks()
      } catch (err) {
        router.push("/auth/signin")
        return
      }
    }
    checkAuth()
  }, [router])

  // Remove the separate loadTasks useEffect since we call it after auth check

  // Error boundary - catch unhandled errors
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      console.error("Unhandled error:", event.error)
      setHasCriticalError(true)
      setError("An unexpected error occurred. Please refresh the page.")
    }

    window.addEventListener("error", handleError)
    return () => window.removeEventListener("error", handleError)
  }, [])

  const loadTasks = async () => {
    try {
      setLoading(true)
      setError("")
      const response = await authenticatedFetch("/api/v1/tasks")

      if (!response.ok) {
        if (response.status === 401) {
          router.push("/auth/signin")
          return
        }
        throw new Error("Failed to load tasks")
      }

      const data = await response.json()
      setTasks(data)
    } catch (err: any) {
      setError(err.message || "Failed to load tasks. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (data: TaskCreate | TaskUpdate) => {
    try {
      setIsCreating(true)
      setError("")

      const response = await authenticatedFetch("/api/v1/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        if (response.status === 401) {
          router.push("/auth/signin")
          return
        }
        const errorData = await response.json().catch(() => ({ detail: "Failed to create task" }))
        throw new Error(errorData.detail || "Failed to create task")
      }

      const newTask = await response.json()
      setTasks([newTask, ...tasks])
    } catch (err: any) {
      setError(err.message || "Failed to create task. Please try again.")
      throw err
    } finally {
      setIsCreating(false)
    }
  }

  const handleToggleComplete = async (id: number) => {
    // Find the task to toggle
    const task = tasks.find((t) => t.id === id)
    if (!task) return

    // Save original tasks for rollback
    const originalTasks = [...tasks]

    try {
      setError("")

      // Optimistic update - immediately update UI
      setTasks(
        tasks.map((t) =>
          t.id === id ? { ...t, completed: !t.completed } : t
        )
      )

      // Make API call
      const response = await authenticatedFetch(`/api/v1/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed: !task.completed }),
      })

      if (!response.ok) {
        if (response.status === 401) {
          router.push("/auth/signin")
          return
        }
        throw new Error("Failed to update task")
      }

      // Update with server response
      const updatedTask = await response.json()
      setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
    } catch (err: any) {
      // Rollback optimistic update on error
      setTasks(originalTasks)
      setError(err.message || "Failed to update task. Please try again.")
    }
  }

  const handleEditTask = async (id: number, data: TaskUpdate) => {
    try {
      setError("")

      const response = await authenticatedFetch(`/api/v1/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        if (response.status === 401) {
          router.push("/auth/signin")
          return
        }
        const errorData = await response.json().catch(() => ({ detail: "Failed to update task" }))
        throw new Error(errorData.detail || "Failed to update task")
      }

      const updatedTask = await response.json()
      setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
      setEditingTaskId(null)
    } catch (err: any) {
      setError(err.message || "Failed to update task. Please try again.")
      throw err
    }
  }

  const handleDeleteTask = async (id: number) => {
    try {
      setError("")

      const response = await authenticatedFetch(`/api/v1/tasks/${id}`, {
        method: "DELETE",
      })

      if (!response.ok) {
        if (response.status === 401) {
          router.push("/auth/signin")
          return
        }
        if (response.status === 404) {
          throw new Error("Task not found. It may have been already deleted.")
        }
        if (response.status === 403) {
          throw new Error("You don't have permission to delete this task")
        }
        throw new Error("Failed to delete task")
      }

      // Remove task from list
      setTasks(tasks.filter((t) => t.id !== id))
    } catch (err: any) {
      setError(err.message || "Failed to delete task. Please try again.")
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
            <p className="mt-2 text-sm text-gray-600">
              Manage your tasks and track your progress
            </p>
          </div>

          {error && (
            <div className="mb-6 rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                  <button
                    onClick={() => setError("")}
                    className="mt-2 text-sm text-red-600 underline hover:text-red-500"
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Create Task Form */}
          <div className="mb-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Task</h2>
            <TaskForm
              mode="create"
              onSubmit={handleCreateTask}
              loading={isCreating}
            />
          </div>

          <TaskList
            tasks={tasks}
            loading={loading}
            onToggle={handleToggleComplete}
            onEdit={handleEditTask}
            onDelete={handleDeleteTask}
            editingTaskId={editingTaskId}
            onEditingChange={setEditingTaskId}
          />
        </div>
      </div>
    </div>
  )
}
