import { useState } from 'react';
import type { FormEvent } from 'react';
import type { Priority, Task, TaskCreate, TaskUpdate } from '../types';

interface CreateProps {
  mode: 'create';
  onSubmit: (values: TaskCreate) => void;
}

interface EditProps {
  mode: 'edit';
  task: Task;
  onSubmit: (values: TaskUpdate) => void;
}

type TaskFormModalProps = (CreateProps | EditProps) & {
  onClose: () => void;
  isPending: boolean;
  errorMessage?: string | null;
};

export function TaskFormModal(props: TaskFormModalProps) {
  const { mode, onClose, isPending, errorMessage } = props;
  const existing = mode === 'edit' ? props.task : undefined;

  const [name, setName] = useState(existing?.name ?? '');
  const [description, setDescription] = useState(existing?.description ?? '');
  const [priority, setPriority] = useState<Priority>(existing?.priority ?? 'medium');

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (props.mode === 'create') {
      props.onSubmit({ name, description, priority });
    } else {
      props.onSubmit({ name, description, priority });
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4">
      <div className="w-full max-w-md rounded-lg bg-white p-5 shadow-xl">
        <h2 className="text-base font-semibold text-slate-900">
          {mode === 'create' ? 'New task' : 'Edit task'}
        </h2>

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div>
            <label htmlFor="task-name" className="block text-sm font-medium text-slate-700">
              Name
            </label>
            <input
              id="task-name"
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
            />
          </div>

          <div>
            <label htmlFor="task-description" className="block text-sm font-medium text-slate-700">
              Description
            </label>
            <textarea
              id="task-description"
              required
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
            />
          </div>

          <div>
            <label htmlFor="task-priority" className="block text-sm font-medium text-slate-700">
              Priority
            </label>
            <select
              id="task-priority"
              value={priority}
              onChange={(e) => setPriority(e.target.value as Priority)}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          {errorMessage && <p className="text-sm text-red-600">{errorMessage}</p>}

          <div className="flex justify-end gap-2 pt-1">
            <button
              type="button"
              onClick={onClose}
              className="rounded-md px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isPending}
              className="rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-60"
            >
              {isPending ? 'Saving…' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
