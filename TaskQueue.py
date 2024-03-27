from dataclasses import dataclass


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


class TaskQueue:

    def __init__(self):
        self._queue = []

    def get_queue_length(self):
        return len(self._queue)

    def add_task(self, task: Task):

        for t in self._queue:
            if t.id == task.id:
                raise DuplicateIdException(f"duplicate id {task.id} found in add_task")

        self._queue.append(task)

    def get_task(self, available_resources: Resources) -> [Task, None]:
        if not self._queue:
            return None

        sq = sorted(self._queue, key=lambda t: t.priority, reverse=True)
        for t in sq:
            if t.resources <= available_resources:
                self._queue.remove(t)
                return t

        return None