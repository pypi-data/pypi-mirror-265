from typing import Annotated
import time

from fastapi import APIRouter, Depends, HTTPException
from threadmem import RoleThread

from guisurfer.server.models import (
    V1UserProfile,
    TaskModel,
    TasksModel,
    TaskCreateModel,
    TaskUpdateModel,
    PostMessageModel,
)
from guisurfer.agent.task import Task
from guisurfer.agent.base import TaskAgentInstance
from guisurfer.agent.runtime import AgentRuntime
from guisurfer.agent.models import SolveTaskModel
from guisurfer.server.models import AddWorkThreadModel, RemoveWorkThreadModel
from guisurfer.auth.transport import get_current_user

router = APIRouter()


@router.post("/v1/tasks", response_model=TaskModel)
async def create_task(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: TaskCreateModel,
):
    task = Task(
        owner_id=current_user.email,
        description=data.description,
        url=data.url,
        status="created",
        created=time.time(),
        started=0.0,
        completed=0.0,
        error="",
        output="",
        assigned_to=data.assigned_to,
    )

    if data.assigned_to:
        found = TaskAgentInstance.find(
            owner_id=current_user.email, name=data.assigned_to
        )
        if not found:
            raise HTTPException(
                status_code=404, detail=f"Assigned agent {data.assigned_to} not found"
            )
        agent = found[0]
        runtimes = AgentRuntime.find_for_user(
            user_id=current_user.email, name=agent.runtime
        )
        if len(runtimes) == 0:
            raise HTTPException(
                status_code=404, detail=f"Runtime {agent.runtime} not found"
            )
        runtime = runtimes[0]

        runtime.call(
            agent.name,
            "/v1/tasks",
            "POST",
            SolveTaskModel(task.to_schema()).model_dump(),
        )

    return task.to_schema()


@router.get("/v1/tasks", response_model=TasksModel)
async def get_tasks(current_user: Annotated[V1UserProfile, Depends(get_current_user)]):
    tasks = Task.find(owner_id=current_user.email)
    return TasksModel(tasks=[task.to_schema() for task in tasks])


@router.get("/v1/tasks/{task_id}", response_model=TaskModel)
async def get_task(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], task_id: str
):
    print("\nfinding task by id: ", task_id)
    tasks = Task.find(id=task_id, owner_id=current_user.email)
    print("\n!! found tasks: ", tasks)
    if not tasks:
        print("\ndid not find task by id: ", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    print("\nfound task by id: ", tasks[0])
    return tasks[0].to_schema()


@router.delete("/v1/tasks/{task_id}")
async def delete_task(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], task_id: str
):
    Task.delete(id=task_id, owner_id=current_user.email)
    return {"message": "Task deleted successfully"}


@router.put("/v1/tasks/{task_id}", response_model=TaskModel)
async def update_task(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    task_id: str,
    data: TaskUpdateModel,
):
    print("\n updating task with model: ", data)
    task = Task.find(id=task_id, owner_id=current_user.email)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = task[0]

    print("\nfound task: ", task.__dict__)
    if data.description:
        task.description = data.description
    if data.status:
        task.status = data.status
    if data.assigned_to:
        task.assigned_to = data.assigned_to
    if data.error:
        task.error = data.error
    if data.output:
        task.output = data.output
    if data.completed:
        task.completed = data.completed
    print("\nsaving task: ", task.__dict__)
    task.save()
    return task.to_schema()


@router.post("/v1/tasks/{task_id}/msg")
async def post_task_msg(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    task_id: str,
    data: PostMessageModel,
):
    print("\n posting message to task: ", data)
    task = Task.find(id=task_id, owner_id=current_user.email)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = task[0]

    if data.thread:
        for thread in task.work_threads:
            if thread.id == data.thread or thread.name == data.thread:
                thread.post(data.role, data.msg, data.images)
                print("\nposted message to thread: ", thread.__dict__)
                return
        raise HTTPException(status_code=404, detail=f"Thread {data.thread} not found")
    task.post_message(data.role, data.msg, data.images)
    print("\nposted message to task: ", task.__dict__)
    return


@router.post("/v1/tasks/{task_id}/threads")
async def create_work_thread(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    task_id: str,
    data: AddWorkThreadModel,
):
    print("\n posting message to task: ", data)
    task = Task.find(id=task_id, owner_id=current_user.email)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = task[0]
    task.create_work_thread(data.name, data.public, data.metadata)
    print("\nadded work thread: ", task.__dict__)
    return


@router.delete("/v1/tasks/{task_id}/threads")
async def remove_work_thread(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    task_id: str,
    data: RemoveWorkThreadModel,
):
    print("\n posting message to task: ", data)
    task = Task.find(id=task_id, owner_id=current_user.email)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = task[0]
    task.remove_work_thread(data.id)
    return
