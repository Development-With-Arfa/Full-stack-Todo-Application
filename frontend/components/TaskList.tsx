import { TaskListProps } from "@/lib/types"
import TaskCard from "./TaskCard"
import EmptyState from "./EmptyState"
import LoadingSpinner from "./LoadingSpinner"

export default function TaskList({
  tasks,
  loading,
  onToggle,
  onEdit,
  onDelete,
  editingTaskId,
  onEditingChange,
}: TaskListProps) {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (tasks.length === 0) {
    return <EmptyState message="No tasks yet. Create your first task above!" />
  }

  return (
    <div className="space-y-4 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-4 md:space-y-0">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
          isEditing={editingTaskId === task.id}
          onEditModeChange={(editing) => onEditingChange(editing ? task.id : null)}
        />
      ))}
    </div>
  )
}
