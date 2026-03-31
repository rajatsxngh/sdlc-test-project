"""In-memory task storage."""

from taskflow.models import Task, TaskCreate


class TaskStorage:
    """Simple in-memory dict-based task store."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, data: TaskCreate) -> Task:
        """Create a new task and return it."""
        task = Task(id=self._next_id, **data.model_dump())
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks ordered by id."""
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task | None:
        """Return a single task by id, or None if not found."""
        return self._tasks.get(task_id)

    # TODO: def update_task(self, task_id: int, data: TaskUpdate) -> Task | None:
    # TODO: def delete_task(self, task_id: int) -> bool:
    # TODO: def search_tasks(self, query: str) -> list[Task]:
    # TODO: def get_stats(self) -> dict:
    # TODO: def export_csv(self) -> str:


storage = TaskStorage()
