import { authClient } from "./auth-client"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function authenticatedFetch(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  // Get JWT token from Better Auth
  const { data } = await authClient.token()

  if (!data?.token) {
    throw new Error("Not authenticated")
  }

  // Attach token to Authorization header
  const headers = new Headers(options.headers)
  headers.set("Authorization", `Bearer ${data.token}`)
  headers.set("Content-Type", "application/json")

  return fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  })
}

// Helper functions for task operations
export async function getTasks() {
  const response = await authenticatedFetch("/api/v1/tasks")
  if (!response.ok) throw new Error("Failed to fetch tasks")
  return response.json()
}

export async function createTask(title: string, description?: string) {
  const response = await authenticatedFetch("/api/v1/tasks", {
    method: "POST",
    body: JSON.stringify({ title, description }),
  })
  if (!response.ok) throw new Error("Failed to create task")
  return response.json()
}

export async function updateTask(id: number, updates: { title?: string; description?: string; completed?: boolean }) {
  const response = await authenticatedFetch(`/api/v1/tasks/${id}`, {
    method: "PUT",
    body: JSON.stringify(updates),
  })
  if (!response.ok) throw new Error("Failed to update task")
  return response.json()
}

export async function deleteTask(id: number) {
  const response = await authenticatedFetch(`/api/v1/tasks/${id}`, {
    method: "DELETE",
  })
  if (!response.ok) throw new Error("Failed to delete task")
}
