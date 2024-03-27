import boto3
from datetime import datetime, timedelta

client = boto3.client('logs', region_name='ap-northeast-2')

def get_log_events(function_name: str):
    try:
        log_group_name = '/aws/lambda/' + function_name

        start_time = int((datetime.today() - timedelta(days=1)).timestamp() * 1000)  # 1일 전부터
        end_time = int(datetime.now().timestamp() * 1000)  # 현재까지

        response = client.filter_log_events(
            logGroupName=log_group_name,
            startTime=start_time,
            endTime=end_time,
            limit=30  # 가져올 로그 이벤트 수 제한
        )

        # for event in response['events']:
        #     print(event['message'])

        print("✅ Successfully get log events")
        return response
    except Exception as e:
        print(f"❌ Error get_log_events: {e}")
        raise Exception("Error get_log_events")
