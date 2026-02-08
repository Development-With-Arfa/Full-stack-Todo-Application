import { TaskCardProps } from "@/lib/types"
import TaskForm from "./TaskForm"

export default function TaskCard({ task, onToggle, onEdit, onDelete, isEditing, onEditModeChange }: TaskCardProps) {
  // Format date to human-readable format
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInMs = now.getTime() - date.getTime()
    const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))

    if (diffInDays === 0) return "Today"
    if (diffInDays === 1) return "Yesterday"
    if (diffInDays < 7) return `${diffInDays} days ago`
    if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`
    if (diffInDays < 365) return `${Math.floor(diffInDays / 30)} months ago`
    return date.toLocaleDateString()
  }

  const handleToggle = () => {
    onToggle(task.id)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === " " || e.key === "Spacebar") {
      e.preventDefault()
      handleToggle()
    }
  }

  const handleEdit = () => {
    onEditModeChange(true)
  }

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      onDelete(task.id)
    }
  }

  const handleSave = async (data: any) => {
    await onEdit(task.id, data)
    onEditModeChange(false)
  }

  const handleCancel = () => {
    onEditModeChange(false)
  }

  // Edit mode - show TaskForm inline
  if (isEditing) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <h3 className="text-sm font-medium text-gray-700 mb-4">Edit Task</h3>
        <TaskForm
          mode="edit"
          initialData={{ title: task.title, description: task.description }}
          onSubmit={handleSave}
          onCancel={handleCancel}
          loading={false}
        />
      </div>
    )
  }

  // Display mode
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="space-y-2">
        <div className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            onKeyDown={handleKeyDown}
            aria-label={`Mark "${task.title}" as ${task.completed ? "incomplete" : "complete"}`}
            className="mt-1 h-4 w-4 text-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 border-gray-300 rounded cursor-pointer"
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between">
              <h3
                className={`text-lg font-medium ${
                  task.completed ? "line-through text-gray-500" : "text-gray-900"
                }`}
              >
                {task.title}
              </h3>
              {task.completed && (
                <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Completed
                </span>
              )}
            </div>

            {task.description && (
              <p className={`text-sm mt-1 ${task.completed ? "text-gray-400" : "text-gray-600"}`}>
                {task.description}
              </p>
            )}

            <div className="flex items-center justify-between pt-2 mt-2 border-t border-gray-100">
              <span className="text-xs text-gray-500">
                Created {formatDate(task.created_at)}
              </span>
              <div className="flex gap-2">
                <button
                  onClick={handleEdit}
                  aria-label={`Edit task "${task.title}"`}
                  className="text-sm text-blue-600 hover:text-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded px-2 py-1"
                >
                  Edit
                </button>
                <button
                  onClick={handleDelete}
                  aria-label={`Delete task "${task.title}"`}
                  className="text-sm text-red-600 hover:text-red-800 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 rounded px-2 py-1"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
