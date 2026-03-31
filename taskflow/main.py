"""FastAPI application for TaskFlow."""

from fastapi import FastAPI, HTTPException

from taskflow.models import Task, TaskCreate
from taskflow.storage import storage

app = FastAPI(title="TaskFlow", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate) -> Task:
    return storage.create_task(data)


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return storage.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# TODO: PUT /tasks/{task_id} - update a task
# TODO: DELETE /tasks/{task_id} - delete a task
# TODO: GET /tasks?status=todo&priority=high - filter tasks
# TODO: GET /tasks/search?q=keyword - search tasks
# TODO: GET /tasks/stats - task statistics
# TODO: GET /tasks/export - CSV export
