import boto3

lambda_client = boto3.client('lambda')

def create_lambda_function(function_name, script, user_env_vars):
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.11',
        Role='arn:aws:iam::860787305217:user/Xnippet',
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': script},
        Description='A Lambda function to run user script.',
        Timeout=60,
        MemorySize=128,
        Environment=user_env_vars
    )
    return response

