import json

import pika
from abc import ABC, abstractmethod

from ai_model_worker.config import AMQP_URL


class BaseWorker(ABC):

    def __init__(self, model_name, callback):
        self.model_name = model_name
        self.callback = callback
        self.connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=model_name)
        self.startup()

    def get_worker_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def startup(self) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    def on_request(self, ch, method, props, body):
        msg = body
        print(f"body : {msg}")

        response = self.callback(msg)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def work(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.model_name, on_message_callback=self.on_request)
        self.channel.start_consuming()
