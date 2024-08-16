from enum import Enum

from keys.keys import TOPICS_LIST, GROUP_ID, BOOTSTRAP_SERVER, SCHEMA_REGISTRY_URL
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.serialization import (
    StringDeserializer,
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from threading import Thread
from event.event import Event
from process_queue.queue_manager import QueueManager
from process_queue.queue_processor import QueueProcessor


class ConsumeManager(object):

    def __init__(self):
        self.consumers = {}
        for topic in TOPICS_LIST:
            self.consumers[topic] = _get_consumer()
            self.consumers[topic].subscribe([topic])
        self.queue_manager = QueueManager()
        self.queue_processor = QueueProcessor(self.queue_manager)

    def start_consumption_all_consumers(self):
        self.queue_processor.start()
        self.queue_processor.running = True
        schema_registry_conf = _get_schema_config()
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        value_deserializer = JSONDeserializer(
            schema_str=_get_schema(),
            from_dict=dict_to_event,
            schema_registry_client=schema_registry_client
        )
        thread_list = []
        for topic, consumer in self.consumers.items():
            thread_list.append(Thread(target=_start_consumer_thread, args=(topic, consumer, value_deserializer, self.queue_manager)))
            thread_list[-1].start()

        for thread in thread_list:
            thread.join()


def _get_consumer():
    consumer = Consumer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "group.id": GROUP_ID,
            "auto.offset.reset": "earliest",
        }
    )
    return consumer


def _start_consumer_thread(topic, consumer, value_deserializer, queue_manager):
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            event = value_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            _process_event(topic, event, queue_manager)

    except KeyboardInterrupt:
        print("Consumer interrupted by user")


def _process_event(topic, event, queue_manager):
    if event is None:
        return

    if event.event_type == "Post" or event.event_type == "Follow" or event.event_type == "Unfollow" or event.event_type == "Live_video" or event.event_type == "Like" or event.event_type == "Comment":
        queue = queue_manager.get_queue("email", topic)
        print("event added to queue")
        queue.put(event)


def _get_schema():
    schema_str = """
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "Event",
      "description": "Notification Event",
      "type": "object",
      "properties": {
        "event_type": {
          "type": "string",
          "enum": ["Post", "Follow", "Unfollow", "Live_video", "Like", "Comment"],
          "description": "Event type"
        },
        "initiated_by": {
          "description": "User who initiated the event",
          "type": "integer"
        },
        "initiated_at": {
          "description": "Time the event was initiated",
          "type": "string"
        },
        "target_group": {
          "type": "integer",
          "description": "The target group of the event"
        }
      },
      "required": ["event_type", "initiated_by", "initiated_at"],
      "additionalProperties": true
    }
    """
    return schema_str


def dict_to_event(obj, ctx):
    if obj is None:
        return None
    return Event(event_type=obj['event_type'], initiated_by=obj['initiated_by'], initiated_at=obj['initiated_at'],
                 target_group=obj['target_group'])


def _get_schema_config():
    schema_registry_conf = {
        "url": SCHEMA_REGISTRY_URL
    }
    return schema_registry_conf
