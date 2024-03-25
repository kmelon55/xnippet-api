from pydantic import BaseModel, Json
from typing import Optional

class Snippet_deploy_request(BaseModel):
  function_name: str
  user_code: str
  user_env_vars: Optional[Json] = None


class Snippet_update_request(BaseModel):
  function_name: str
  user_code: Optional[str] = None
  user_env_vars: Optional[Json] = None


class Snippet_delete_request(BaseModel):
  function_name: str