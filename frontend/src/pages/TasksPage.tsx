import { useMemo, useState } from 'react';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { TaskFormModal } from '../components/TaskFormModal';
import { TaskList } from '../components/TaskList';
import { getErrorMessage } from '../api/client';
import { useCreateTask, useDeleteTask, useTasks, useUpdateTask } from '../hooks/useTasks';
import type { Task, TaskCreate, TaskUpdate } from '../types';

type Filter = 'all' | 'active' | 'completed';

const FILTERS: { value: Filter; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'active', label: 'Active' },
  { value: 'completed', label: 'Completed' },
];

export function TasksPage() {
  const { data: tasks, isLoading, isError, error } = useTasks();
  const createTask = useCreateTask();
  const updateTask = useUpdateTask();
  const deleteTask = useDeleteTask();

  const [filter, setFilter] = useState<Filter>('all');
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const visibleTasks = useMemo(() => {
    if (!tasks) return [];
    if (filter === 'active') return tasks.filter((t) => !t.completed);
    if (filter === 'completed') return tasks.filter((t) => t.completed);
    return tasks;
  }, [tasks, filter]);

  function handleCreate(values: TaskCreate) {
    setFormError(null);
    createTask.mutate(values, {
      onSuccess: () => setIsCreateOpen(false),
      onError: (err) => setFormError(getErrorMessage(err)),
    });
  }

  function handleEditSubmit(values: TaskUpdate) {
    if (!editingTask) return;
    setFormError(null);
    updateTask.mutate(
      { id: editingTask.id, payload: values },
      {
        onSuccess: () => setEditingTask(null),
        onError: (err) => setFormError(getErrorMessage(err)),
      },
    );
  }

  function handleToggleCompleted(task: Task) {
    updateTask.mutate({ id: task.id, payload: { completed: !task.completed } });
  }

  function handleConfirmDelete() {
    if (!deletingTask) return;
    deleteTask.mutate(deletingTask.id, { onSuccess: () => setDeletingTask(null) });
  }

  return (
    <div className="mx-auto mt-8 w-full max-w-3xl px-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-slate-900">Your tasks</h1>
        <button
          type="button"
          onClick={() => {
            setFormError(null);
            setIsCreateOpen(true);
          }}
          className="rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-slate-800"
        >
          New task
        </button>
      </div>

      <div className="mt-4 flex gap-1">
        {FILTERS.map((f) => (
          <button
            key={f.value}
            type="button"
            onClick={() => setFilter(f.value)}
            className={`rounded-md px-3 py-1.5 text-sm font-medium ${
              filter === f.value
                ? 'bg-slate-900 text-white'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="mt-4">
        {isLoading && <p className="text-sm text-slate-500">Loading tasks…</p>}
        {isError && <p className="text-sm text-red-600">{getErrorMessage(error)}</p>}
        {!isLoading && !isError && (
          <TaskList
            tasks={visibleTasks}
            onToggleCompleted={handleToggleCompleted}
            onEdit={(task) => {
              setFormError(null);
              setEditingTask(task);
            }}
            onDelete={(task) => setDeletingTask(task)}
          />
        )}
      </div>

      {isCreateOpen && (
        <TaskFormModal
          mode="create"
          onSubmit={handleCreate}
          onClose={() => setIsCreateOpen(false)}
          isPending={createTask.isPending}
          errorMessage={formError}
        />
      )}

      {editingTask && (
        <TaskFormModal
          mode="edit"
          task={editingTask}
          onSubmit={handleEditSubmit}
          onClose={() => setEditingTask(null)}
          isPending={updateTask.isPending}
          errorMessage={formError}
        />
      )}

      {deletingTask && (
        <ConfirmDialog
          title="Delete task"
          message={`Delete "${deletingTask.name}"? This can't be undone.`}
          confirmLabel="Delete"
          isPending={deleteTask.isPending}
          onConfirm={handleConfirmDelete}
          onCancel={() => setDeletingTask(null)}
        />
      )}
    </div>
  );
}
