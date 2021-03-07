#!/user/bin/python
# -*-coding:UTF-8-*-
"""
@Author:    Night Cruising
@File:      rpc_server.py
@Time:      2021/3/7 0007
@Version:   3.7.3
@Desc:      None
"""
import os

import pika

from settings import SERVER_HOST, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, EXCHANGE_NAME


class RpcServer(object):
    def __init__(self):
        self._initial()

    def _initial(self):
        credentials = pika.PlainCredentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
        )
        self.channel = connection.channel()
        queue = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = queue.method.queue
        self.channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='direct',
        )
        self.channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=queue_name,
            routing_key=SERVER_HOST,
        )
        self.channel.basic_consume(
            on_message_callback=self.hanle_response,
            queue=queue_name
        )

    def hanle_response(self, ch, method, properties, body):
        command = body.decode()
        command_result = self.handle_command(command=command)
        self.channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            ),
            body=command_result.encode()
        )

    @staticmethod
    def handle_command(command: str):
        return os.popen(command).read()
