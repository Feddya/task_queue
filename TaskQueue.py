from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(eq=True, order=True, frozen=True)
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass(eq=True, order=True, frozen=False)
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str


class DuplicateIdException(Exception):
    pass


class QueueImplementationBase(ABC):

    @abstractmethod
    def get_queue_length(self) -> int:
        pass

    @abstractmethod
    def add_task(self, task: Task) -> None:
        pass

    @abstractmethod
    def is_task_already_added(self, task: Task) -> bool:
        pass

    @abstractmethod
    def get_task(self, available_resources: Resources) -> [Task, None]:
        pass


class ListQueue(QueueImplementationBase):

    def __init__(self):
        self._queue = []

    def get_queue_length(self) -> int:
        return len(self._queue)

    def add_task(self, task: Task) -> None:

        self._queue.append(task)

    def is_task_already_added(self, task: Task) -> bool:
        for t in self._queue:
            if t.id == task.id:
                return True

        return False

    def get_task(self, available_resources: Resources) -> [Task, None]:
        if not self._queue:
            return None

        sq = sorted(self._queue, key=lambda t: t.priority, reverse=True)
        for t in sq:
            if t.resources <= available_resources:
                self._queue.remove(t)
                return t

        return None


class TaskQueue:

    def __init__(self):
        self._queue = ListQueue()

    def get_queue_length(self) -> int:
        return self._queue.get_queue_length()

    def add_task(self, task: Task) -> None:

        if self._queue.is_task_already_added(task):
            raise DuplicateIdException(f"duplicate id {task.id} found in add_task")

        self._queue.add_task(task)

    def get_task(self, available_resources: Resources) -> [Task, None]:
        return self._queue.get_task(available_resources)