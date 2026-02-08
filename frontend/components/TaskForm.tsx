import { useState, useEffect } from "react"
import { TaskFormProps, TaskCreate, TaskUpdate } from "@/lib/types"
import LoadingSpinner from "./LoadingSpinner"

export default function TaskForm({
  onSubmit,
  initialData,
  loading,
  onCancel,
  mode,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "")
  const [description, setDescription] = useState(initialData?.description || "")
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({})

  // Update form when initialData changes (for edit mode)
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || "")
      setDescription(initialData.description || "")
    }
  }, [initialData])

  const validate = (): boolean => {
    const newErrors: { title?: string; description?: string } = {}

    if (!title.trim()) {
      newErrors.title = "Title is required"
    } else if (title.length > 255) {
      newErrors.title = "Title must be 255 characters or less"
    }

    if (description && description.length > 1000) {
      newErrors.description = "Description must be 1000 characters or less"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) {
      return
    }

    const data: TaskCreate | TaskUpdate = {
      title: title.trim(),
      description: description.trim() || undefined,
    }

    await onSubmit(data)

    // Reset form after successful creation (create mode only)
    if (mode === "create") {
      setTitle("")
      setDescription("")
      setErrors({})
    }
  }

  const handleCancel = () => {
    if (onCancel) {
      setTitle(initialData?.title || "")
      setDescription(initialData?.description || "")
      setErrors({})
      onCancel()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={loading}
          className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm ${
            errors.title
              ? "border-red-300 focus:border-red-500 focus:ring-red-500"
              : "border-gray-300 focus:border-blue-500"
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          placeholder="Enter task title"
          maxLength={255}
        />
        {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
        <p className="mt-1 text-xs text-gray-500">{title.length}/255 characters</p>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
          rows={3}
          className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm ${
            errors.description
              ? "border-red-300 focus:border-red-500 focus:ring-red-500"
              : "border-gray-300 focus:border-blue-500"
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          placeholder="Enter task description"
          maxLength={1000}
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">{description.length}/1000 characters</p>
      </div>

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <LoadingSpinner size="sm" className="mr-2" />
              {mode === "create" ? "Adding..." : "Saving..."}
            </>
          ) : mode === "create" ? (
            "Add Task"
          ) : (
            "Save Changes"
          )}
        </button>

        {mode === "edit" && onCancel && (
          <button
            type="button"
            onClick={handleCancel}
            disabled={loading}
            className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}
