import time
from threading import Thread
import keys.keys as keys
from email_service import aws_sqs


class QueueProcessor:
    def __init__(self, queue_manager):
        self.queue_manager = queue_manager
        self.running = False
        self.threads = []

    def start(self):
        self.running = True
        for service in keys.NOTIFICATION_SERVICES:
            for topic in keys.TOPICS_LIST:
                thread = Thread(target=self._process_queue, args=(service, topic))
                thread.start()
                self.threads.append(thread)

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()

    def _process_queue(self, service, topic):
        while self.running:
            queue = self.queue_manager.get_queue(service, topic)
            if not queue.empty():
                event = queue.get()
                aws_sqs.send_message(event)
                print(f"Processing event for {service} service, topic {topic}: {event}")
            time.sleep(1)