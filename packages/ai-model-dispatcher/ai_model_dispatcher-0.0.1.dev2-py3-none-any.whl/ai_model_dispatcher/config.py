import os

AMQP_URL = os.getenv('AMQP_URL', 'amqp://app:123456@localhost:5672/')
