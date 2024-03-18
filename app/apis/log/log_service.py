import boto3
from datetime import datetime, timedelta

# CloudWatch Logs 클라이언트 생성
client = boto3.client('logs', region_name='ap-northeast-2')


def get_log_events(function_name: str):

    # 로그 그룹 이름 및 시간 범위 설정
    # 예를 들어, '/aws/lambda/your_lambda_function_name'과 같이 설정합니다.
    log_group_name = '/aws/lambda/' + function_name
    start_time = int((datetime.today() - timedelta(days=1)).timestamp() * 1000)  # 1일 전부터
    end_time = int(datetime.now().timestamp() * 1000)  # 현재까지

    # 로그 이벤트 가져오기
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        limit=30  # 가져올 로그 이벤트 수 제한
    )

    # for event in response['events']:
    #     print(event['message'])

    return response