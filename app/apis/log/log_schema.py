from pydantic import BaseModel, Json
from typing import Optional

class GetLogsRequest(BaseModel):
    function_name: str