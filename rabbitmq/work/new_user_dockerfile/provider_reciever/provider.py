import pika

credentials = pika.PlainCredentials('yet', 'asdfasdf')

parameters = pika.ConnectionParameters(
	'172.17.0.1',
	port=5672,
	credentials=credentials
)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

exchange_name = 'create_user'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct',
)

channel.basic_publish(
    exchange=exchange_name,
    routing_key=exchange_name,
    body=exchange_name,
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)

print(exchange_name)

connection.close()
