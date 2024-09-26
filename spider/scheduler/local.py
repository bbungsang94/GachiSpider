import json
import boto3
from .engine import Engine

class LambdaScheduler:
    def __init__(self, db_ip: str, db_port: int):
        self.engine = Engine(period=1.0, name="lambda-crawler")
        self.db_ip, self.db_port = db_ip, db_port
    
    def parse(self, url):
        self.engine.add_event(self._invoke, "lambda-crawl",
                              url=url, db_ip=self.db_ip, db_port=self.db_port)
        self.engine.run()
        pass
    
    def _invoke(**kwargs):
        # Lambda 클라이언트 생성
        lambda_client = boto3.client('lambda', region_name='ap-northeast-2')  # 예: 'us-east-1'

        # 이벤트로 URL을 Lambda에 전달
        payload = kwargs
        
        try:
            # Lambda 함수 호출
            response = lambda_client.invoke(
                FunctionName='lambdaParser',  # 배포한 Lambda 함수의 이름
                InvocationType='RequestResponse',  # 동기 호출
                Payload=json.dumps(payload)  # 이벤트로 보낼 페이로드 (JSON으로 직렬화)
            )
            
            # 응답 처리
            response_payload = json.loads(response['Payload'].read())
            if response_payload['statusCode'] == 200:
                print(f"Lambda Function Success: {response_payload['body']}")
                print(f"File saved at: {response_payload['file_path']}")
            else:
                print(f"Lambda Function Error: {response_payload['body']}")
        
        except Exception as e:
            print(f"Error invoking Lambda function: {str(e)}")


if __name__ == "__main__":
    scheduler = LambdaScheduler(db_ip="110.165.19.253", db_port=27017)
    scheduler.parse(url="https://www.todayhumor.co.kr/board/view.php?table=humordata&no=2025625&s_no=2025625")