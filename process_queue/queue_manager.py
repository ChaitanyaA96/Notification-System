from process_queue import ProcessQueue as pq
import keys.keys as keys


class QueueManager:

    def __init__(self):
        self.queues = {}
        for service in keys.NOTIFICATION_SERVICES:
            for topic in keys.TOPICS_LIST:
                self.queues[service] = {topic: pq()}

    def get_queue(self, service, topic):
        return self.queues[service][topic]

