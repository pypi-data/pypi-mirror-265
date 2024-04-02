from __future__ import annotations

import os
import json
import pika
import time

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from pika.exchange_type import ExchangeType
from pika.exceptions import StreamLostError


class Publisher:
    connection: BlockingConnection
    channel: BlockingChannel
    exchange: str

    def __init__(self, exchange: str):
        super().__init__()
        self.exchange = exchange
        self.setup_connection()

    def is_enabled(self) -> bool:
        return bool(int(os.getenv("RABBITMQ_ENABLED", default=0)))

    def setup_connection(self):
        if not self.is_enabled():
            return

        host = os.getenv("RABBITMQ_HOST", default="")
        port = os.getenv("RABBITMQ_PORT", default=0)
        username = os.getenv("RABBITMQ_USERNAME", default="")
        password = os.getenv("RABBITMQ_PASSWORD", default="")

        credentials = pika.PlainCredentials(username=username, password=password)
        parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def declare_exchange(self, exchange_type: ExchangeType = ExchangeType.topic, **kwargs):
        self.channel.exchange_declare(self.exchange, exchange_type=exchange_type, **kwargs)

    def publish(
            self,
            data: dict,
            routing_key: str,
            mandatory: bool = False,
            retry_attempts: int = 5,
            **kwargs,
    ) -> None:
        if not self.is_enabled():
            return

        reconnect_attempts = 0

        while True:
            try:
                data = data or {}
                body = json.dumps(data).encode("utf-8")
                properties = BasicProperties(content_encoding="utf-8", content_type="application/json", **kwargs)
                self.channel.basic_publish(
                    body=body,
                    exchange=self.exchange,
                    routing_key=routing_key,
                    properties=properties,
                    mandatory=mandatory,
                )
                break
            except pika.exceptions.ConnectionClosedByBroker:
                break
            except pika.exceptions.AMQPChannelError:
                break
            except pika.exceptions.AMQPConnectionError:
                if reconnect_attempts < retry_attempts:
                    reconnect_attempts += 1
                    time.sleep(reconnect_attempts / 2)
                    self.setup_connection()  # Recover connection
                    continue
                break
