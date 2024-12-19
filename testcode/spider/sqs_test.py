import boto3
import json

# SQS 클라이언트 생성
sqs = boto3.client('sqs', region_name='ap-northeast-2')

# SQS 큐 URL
queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/125501251865/gachiga-crawl-link-parser-queue'

# 메시지 내용
message = {
    "url": "https://aagag.com/mirror/?time=3&site=bobae|clien|humor|inven|mlbpark|ou|ppomppu|ruli&select=multi",
    "db_ip": "mongodb://lakemaster:zmflxh1004!@creadto-gachirok-datalake.cluster-cbtcjvjycynl.ap-northeast-2.docdb.amazonaws.com:27017/?ssl=true&retryWrites=false&tlsAllowInvalidCertificates=true",
    "db_port": None
}

# 메시지 전송
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps(message)  # 메시지를 JSON 문자열로 변환
)

print(f"Message ID: {response['MessageId']}")