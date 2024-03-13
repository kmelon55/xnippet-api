from fastapi import APIRouter
from dotenv import load_dotenv
from starlette.config import Config


from apis.snippet.snippet_service import create_lambda_function 

router = APIRouter(
    prefix="/snippet",
    tags=["lambda function apis"], 
)

@router.post("/deploy")
def deploy_snippet(request):

    function_name = 'test'
    script = 'print(1+1)'
    user_env_vars = {
       'Variables': 'test'
    }

    response = create_lambda_function(function_name, script, user_env_vars)

    return response