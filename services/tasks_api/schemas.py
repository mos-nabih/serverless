from uuid import UUID

from pydantic import BaseModel

from models import TaskStatus


class CreateTask(BaseModel):
    title: str


class CloseTask(BaseModel):
    id: UUID


class APITask(BaseModel):
    id: UUID
    title: str
    status: TaskStatus
    owner: str

    model_config = {"from_attributes": True}


class APITaskList(BaseModel):
    results: list[APITask]

    model_config = {"from_attributes": True}
