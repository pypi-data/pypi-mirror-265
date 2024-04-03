from pydantic import BaseModel
from typing import Optional, List

from guisurfer.server.models import TaskModel, EnvVarOptModel


class SolveTaskModel(BaseModel):
    task: TaskModel
    desktop_name: Optional[str] = None
    max_steps: int = 20
    site: Optional[str] = None
