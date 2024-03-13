import boto3

lambda_client = boto3.client('lambda')

def create_lambda_function(function_name, script, user_env_vars):
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role='arn:aws:iam::123456789012:role/your-lambda-role',
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': script},
        Description='A Lambda function to run user script.',
        Timeout=30,
        MemorySize=128,
        Environment={
            'Variables': user_env_vars
        }
    )
    return response