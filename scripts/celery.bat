rabbitmq-server
d:
cd D:\Creadto\GachiSpider\testcode\lakemaster
celery -A filter worker --loglevel=info --pool=gevent
