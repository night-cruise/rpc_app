#!/user/bin/python
# -*-coding:UTF-8-*-
"""
@Author:    Night Cruising
@File:      rpc_client.py
@Time:      2021/3/7 0007
@Version:   3.7.3
@Desc:      None
"""
import uuid
from typing import Optional

import pika

from settings import RABBITMQ_USERNAME, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT, EXCHANGE_NAME


class RpcClient(object):
    def __init__(self):
        self._initial()
        self.corr_id: Optional[str] = None
        self.response: Optional[str] = None

    def _initial(self):
        credentials = pika.PlainCredentials(
            username=RABBITMQ_USERNAME,
            password=RABBITMQ_PASSWORD
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='direct'
        )

    def send_request(self, command: str, host: str):
        corr_id: str = str(uuid.uuid4())
        queue = self.channel.queue_declare(queue='', exclusive=True)
        callback_queue: str = queue.method.queue
        self.channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=host,
            body=command.encode(),
            properties=pika.BasicProperties(
                correlation_id=corr_id,
                reply_to=callback_queue
            )
        )
        return corr_id, callback_queue

    def get_response(self, corr_id: str, callback_queue: str):
        self.corr_id = corr_id
        self.channel.basic_consume(
            queue=callback_queue,
            on_message_callback=self._handle_response
        )
        self.response = None
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def _handle_response(self, ch, method, properties, body):
        if properties.correlation_id == self.corr_id:
            self.response = body.decode()
