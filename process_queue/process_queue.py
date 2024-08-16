from queue import Queue
from typing import Generic, TypeVar, Any
from event.event import Event


T = TypeVar('T', bound=Event)


class ProcessQueue(Generic[T]):
    def __init__(self):
        self.__queue = Queue()
        self.size = self.__queue.qsize()

    def put(self, event: T) -> None:
        self.__queue.put(event)

    def get(self) -> T:
        return self.__queue.get()

    def empty(self) -> bool:
        return self.__queue.empty()
