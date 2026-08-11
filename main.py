from itertools import count
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A small CRUD API for managing a to-do list. Data lives in memory only — it resets every time the server restarts.",
    version="1.0",
)


# --- in-memory "database" ------------------------------------------------

_next_id = count(1)

tasks: list[dict] = []


def seed_tasks() -> None:
    for title in ["Buy groceries", "Write the README", "Deploy to production"]:
        tasks.append({"id": next(_next_id), "title": title, "done": False})


seed_tasks()


# --- schemas --------------------------------------------------------------

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


class Task(BaseModel):
    id: int
    title: str
    done: bool


# --- error shape ------------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # A missing/malformed request body would normally 422 by default.
    # The assignment spec wants 400 for any invalid create/update request.
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Normalize to {"error": ...} instead of FastAPI's default {"detail": ...}
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


# --- helpers ----------------------------------------------------------------

def find_task(task_id: int) -> Optional[dict]:
    return next((t for t in tasks if t["id"] == task_id), None)


# --- Stage 1: root and health -----------------------------------------------

@app.get("/", description="Describes this API: its name, version, and top-level endpoints.")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", description="Health check — confirms the server is alive.")
def health():
    return {"status": "ok"}


# --- Stage 2: read -----------------------------------------------------------

@app.get("/tasks", response_model=list[Task], description="List every task.")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task, description="Get a single task by id.")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


# --- Stage 3: create -----------------------------------------------------------

@app.post(
    "/tasks",
    response_model=Task,
    status_code=201,
    description="Create a new task. Requires a non-empty title.",
)
def create_task(payload: TaskCreate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")

    task = {"id": next(_next_id), "title": title, "done": False}
    tasks.append(task)
    return task


# --- Stage 4: update & delete -------------------------------------------------

@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    description="Update a task's title and/or done status.",
)
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=400, detail="Provide at least one of: title, done")

    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task["title"] = title

    if payload.done is not None:
        task["done"] = payload.done

    return task


@app.delete("/tasks/{task_id}", status_code=204, description="Delete a task.")
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
