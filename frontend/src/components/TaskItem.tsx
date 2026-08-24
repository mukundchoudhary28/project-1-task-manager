import type { Task } from '../types';
import { PriorityBadge } from './PriorityBadge';

interface TaskItemProps {
  task: Task;
  onToggleCompleted: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
}

export function TaskItem({ task, onToggleCompleted, onEdit, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-start gap-3 rounded-lg border border-slate-200 bg-white p-4">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggleCompleted(task)}
        className="mt-1 h-4 w-4 accent-slate-900"
        aria-label={`Mark "${task.name}" as ${task.completed ? 'active' : 'completed'}`}
      />

      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <p className={`font-medium text-slate-900 ${task.completed ? 'line-through text-slate-400' : ''}`}>
            {task.name}
          </p>
          <PriorityBadge priority={task.priority} />
        </div>
        <p className={`mt-0.5 text-sm text-slate-600 ${task.completed ? 'line-through text-slate-400' : ''}`}>
          {task.description}
        </p>
        <p className="mt-1 text-xs text-slate-400">
          Created {new Date(task.created_at).toLocaleString()}
        </p>
      </div>

      <div className="flex shrink-0 gap-1">
        <button
          type="button"
          onClick={() => onEdit(task)}
          className="rounded-md px-2 py-1 text-sm font-medium text-slate-600 hover:bg-slate-100"
        >
          Edit
        </button>
        <button
          type="button"
          onClick={() => onDelete(task)}
          className="rounded-md px-2 py-1 text-sm font-medium text-red-600 hover:bg-red-50"
        >
          Delete
        </button>
      </div>
    </li>
  );
}
