from pydantic import BaseModel, Json
from typing import Optional

class CodeGenerateRequest(BaseModel):
	code: Optional[str] = None
	user_prompt: str