from fastapi import APIRouter

from apis.snippet.snippet_service import create_zip_file, create_lambda_function, create_lambda_function_url, add_lambda_function_permission, delete_lambda_function, delete_lambda_function_url, update_lambda_function_code, update_lambda_function_configuration
from apis.snippet.snippet_schema import Snippet_deploy_request, Snippet_delete_request, Snippet_update_request

router = APIRouter(
    prefix="/snippet",
    tags=["lambda function apis"], 
)

@router.post("/deploy")
def deploy_lambda_function(request: Snippet_deploy_request):

    function_name = request.function_name
    user_code = request.user_code
    user_env_vars = request.user_env_vars

    zip_file = create_zip_file(user_code)
    lambda_function_response = create_lambda_function(function_name, zip_file, user_env_vars)
    create_lambda_function_url(function_name)
    add_lambda_function_permission(function_name)

    return lambda_function_response,


@router.post("/update")
def update_lambda_function(request: Snippet_update_request):

    function_name = request.function_name
    user_code = request.user_code
    user_env_vars = request.user_env_vars

    zip_file = create_zip_file(user_code)
    response = update_lambda_function_code(function_name, zip_file)
    
    if user_env_vars:
        update_lambda_function_configuration_response = update_lambda_function_configuration(function_name, user_env_vars)

    return response


@router.post("/delete")
def delete_snippet(request: Snippet_delete_request):

    function_name = request.function_name

    delete_lambda_function_url
    response = delete_lambda_function(function_name)
    return response

