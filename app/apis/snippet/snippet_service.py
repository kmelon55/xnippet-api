import boto3
import zipfile
import io
from zipfile import ZipInfo
import textwrap

from dotenv import load_dotenv
from starlette.config import Config

load_dotenv()
config = Config()

http_handler_code_template = """
import json

routes = {}

def route(path, methods=['GET']):
    def decorator(func):
        routes[(path, tuple(methods))] = func
        return func
    return decorator

def lambda_handler(event, context):
    request_method = event.get('httpMethod')
    request_path = event.get('path')
    request_body = event.get('body')
    if request_body:
        request_data = json.loads(request_body)
    else:
        request_data = {}

    handler = routes.get((request_path, request_method.lower()))
    if handler:
        response = handler(request_data)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Not found')
        }

# User code starts here
{user_code}
"""


lambda_handler_template = """
import json

def lambda_handler(event, context):
{user_code}
    return {{
        'statusCode': 200,
        'body': json.dumps('Function executed successfully.')
    }}
"""

def create_zip_file(user_code):
    try:
        zip_output = io.BytesIO()
        zip_file = zipfile.ZipFile(zip_output, 'w')
        
        # 파일에 대한 정보와 권한 설정
        info = ZipInfo('lambda_function.py')
        info.external_attr = 0o755 << 16  # 파일에 실행 권한 부여

        indented_code = textwrap.indent(text=user_code, prefix='    ')
        handler_code = lambda_handler_template.format(user_code=indented_code)

        # 수정된 권한 정보를 사용하여 파일 쓰기
        zip_file.writestr(info, handler_code)
        zip_file.close()
        zip_output.seek(0)
        return zip_output.read()
    except Exception as e:
        print(f"❌ Error creating zip file: {e}")
        raise Exception("Error creating zip file")

lambda_client = boto3.client('lambda', region_name='ap-northeast-2')

##################################################################################################
################################ Create Lambda Function ##########################################
##################################################################################################

def create_lambda_function(function_name, zip_file, user_env_vars=None):
    try:

        function_params = {
            'FunctionName': function_name,
            'Runtime': 'python3.11',
            'Role': config('LAMBDA_ROLE_ARN'),
            'Handler': 'lambda_function.lambda_handler',
            'Code': {'ZipFile': zip_file},
            'Description': 'A Lambda function to run user_code.',
            'Timeout': 60,
            'MemorySize': 128,
        }

        if user_env_vars:
            function_params['Environment'] = user_env_vars

        response = lambda_client.create_function(**function_params)
        print(f"✅ Function {function_name} created successfully.")
    except Exception as e:
        print(f"❌ Error creating function {function_name}: {e}")

    return response


def create_lambda_function_url(function_name):
    try:
        response = lambda_client.create_function_url_config(
            FunctionName=function_name,
            AuthType='NONE'
        )
        print(f"✅ Function URL configuration for {function_name} created successfully.")
        return response
    except Exception as e:
        print(f"❌ Error creating URL configuration for {function_name}: {e}")


def add_lambda_function_permission(function_name):
    response = lambda_client.add_permission(
        FunctionName=function_name,
        StatementId='FunctionURLInvokePermission',
        Action='lambda:invokeFunctionUrl',
        Principal='*',
        FunctionUrlAuthType='NONE',
    )
    return response

##################################################################################################
################################# Get Lambda Function ############################################
##################################################################################################

def get_lambda_function(function_name):
    try:
        response = lambda_client.get_function(FunctionName=function_name)
        print(f"✅ Function {function_name} found.")
        return response
    except Exception as e:
        print(f"❌ Error finding function {function_name}: {e}")

##################################################################################################
################################ Update Lambda Function ##########################################
##################################################################################################

def update_lambda_function_code(function_name, zip_file):
    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_file,
        )
        print(f"✅ Function {function_name} updated successfully.")   
        return response
    except Exception as e:
        print(f"❌ Error updating function {function_name}: {e}")


def update_lambda_function_configuration(function_name, user_env_vars):
    try:
        response = lambda_client.update_function_configuration(
            FunctionName=function_name,
            Environment=user_env_vars
        )
        print(f"✅ Function {function_name} updated successfully.")
        return response
    except Exception as e:
        print(f"❌ Error updating function {function_name}: {e}")


##################################################################################################
################################ Delete Lambda Function ##########################################
##################################################################################################

def delete_lambda_function(function_name):
    try:
        response = lambda_client.delete_function(FunctionName=function_name)
        print(f"✅ Function {function_name} deleted successfully.")
        return response
    except Exception as e:
        print(f"❌ Error deleting function {function_name}: {e}")


def delete_lambda_function_url(function_name):
    try:
        response = lambda_client.delete_function_url_config(FunctionName=function_name)
        print(f"✅ Function URL configuration for {function_name} has been deleted.")
        return response
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"❌ No URL configuration found for {function_name}.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")