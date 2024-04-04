import datetime as dt

from pydantic import BaseModel
from pydantic.types import UUID4

# Extras


class DropDownOption(BaseModel):
    id: UUID4
    name: str
    color: str
    orderindex: int


class DropDownTypeConfig(BaseModel):
    default: int
    options: list[DropDownOption]


class CustomField(BaseModel):
    name: str
    value: str | float | dt.date | None


class Task(BaseModel):
    id: str
    name: str
    status: str
    date_updated: dt.date | None
    date_created: dt.date | None
    custom_fields: list[CustomField]


# Parameters


# Payloads


# Responses
class GetTasksResponse(BaseModel):
    tasks: list[Task]
