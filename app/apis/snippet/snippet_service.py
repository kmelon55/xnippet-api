import boto3
import zipfile
import io

from dotenv import load_dotenv
from starlette.config import Config

load_dotenv()
config = Config('.env')


http_handler_code_template = """
import json
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'GET':
        # GET 요청 처리 로직
        response = handle_get_request(event)
        
    elif http_method == 'POST':
        # POST 요청 처리 로직
        response = handle_post_request(event)
        
    elif http_method == 'PUT':
        # PUT 요청 처리 로직
        response = handle_put_request(event)
        
    elif http_method == 'DELETE':
        # DELETE 요청 처리 로직
        response = handle_delete_request(event)
        
    else:
        response = {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }
"""

def create_zip_file(code):
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, 'w')
    zip_file.writestr('lambda_function.py', code)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read()

lambda_client = boto3.client('lambda', region_name='ap-northeast-2')

##################################################################################################
################################ Create Lambda Function ##########################################
##################################################################################################

def create_lambda_function(function_name, script, user_env_vars=None):
    try:
        zip_file_bytes = create_zip_file(script)

        function_params = {
            'FunctionName': function_name,
            'Runtime': 'python3.11',
            'Role': config('LAMBDA_ROLE_ARN'),
            'Handler': 'lambda_function.lambda_handler',
            'Code': {'ZipFile': zip_file_bytes},
            'Description': 'A Lambda function to run user script.',
            'Timeout': 60,
            'MemorySize': 128,
        }

        if user_env_vars:
            function_params['Environment'] = user_env_vars

        print(f"Function {function_name} created successfully.")
        response = lambda_client.create_function(**function_params)
    except Exception as e:
        print(f"Error creating function {function_name}: {e}")

    return response


def create_lambda_function_url(function_name):
    try:
        response = lambda_client.create_function_url_config(
            FunctionName=function_name,
            AuthType='NONE'
        )
        print(f"Function URL configuration for {function_name} created successfully.")
        return response
    except Exception as e:
        print(f"Error creating URL configuration for {function_name}: {e}")


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
        print(f"Function {function_name} found.")
        return response
    except Exception as e:
        print(f"Error finding function {function_name}: {e}")

##################################################################################################
################################ Update Lambda Function ##########################################
##################################################################################################

def update_lambda_function_code(function_name, script):
    try:
        zip_file_bytes = create_zip_file(script)

        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_file_bytes,
        )
        print(f"Function {function_name} updated successfully.")   
        return response
    except Exception as e:
        print(f"Error updating function {function_name}: {e}")


def update_lambda_function_configuration(function_name, user_env_vars):
    try:
        response = lambda_client.update_function_configuration(
            FunctionName=function_name,
            Environment=user_env_vars
        )
        print(f"Function {function_name} updated successfully.")
        return response
    except Exception as e:
        print(f"Error updating function {function_name}: {e}")


##################################################################################################
################################ Delete Lambda Function ##########################################
##################################################################################################

def delete_lambda_function(function_name):
    try:
        response = lambda_client.delete_function(FunctionName=function_name)
        print(f"Function {function_name} deleted successfully.")
        return response
    except Exception as e:
        print(f"Error deleting function {function_name}: {e}")


def delete_lambda_function_url(function_name):
    try:
        response = lambda_client.delete_function_url_config(FunctionName=function_name)
        print(f"Function URL configuration for {function_name} has been deleted.")
        return response
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"No URL configuration found for {function_name}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")