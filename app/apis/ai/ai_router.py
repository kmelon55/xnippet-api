from fastapi import APIRouter

from apis.ai.ai_schema import CodeGenerateRequest
from apis.ai.ai_service import code_generate

router = APIRouter(
    prefix="/ai",
    tags=["Code generate with AI"], 
)

@router.post("/generate")
def ai_code_generate(request: CodeGenerateRequest):
    print("🚀 ai_code_generate request")

    code = request.code
    user_prompt = request.user_prompt

    response = code_generate(code, user_prompt)
    return response

