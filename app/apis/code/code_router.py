from fastapi import APIRouter
from dotenv import load_dotenv
from starlette.config import Config

from apis.code.code_schema import CodeGenerateRequest

router = APIRouter(
    prefix="/code",
    tags=["Code generate with AI"], 
)

@router.get("/generate")
def code_generate(request: CodeGenerateRequest):
    return

