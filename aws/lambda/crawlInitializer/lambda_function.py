
def lambda_handler(event, context):
    url = event.get('url')
    db_ip = event.get('db_ip')
    db_port = event.get('db_port')
    
    return {'statusCode': 201, 'message': "Get message", 'url': url, 'db_ip': db_ip, 'db_port': db_port}