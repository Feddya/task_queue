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
        self.queue = []

    def add_task(self, task: Task):

        for t in self.queue:
            if t.id == task.id:
                raise DuplicateIdException(f"duplicate id {task.id} found in add_task")

        self.queue.append(task)

    def get_task(self, available_resources: Resources) -> [Task, None]:
        if not self.queue:
            return None

        sq = sorted(self.queue, key=lambda t: t.priority, reverse=True)
        for t in sq:
            if t.resources <= available_resources:
                self.queue.remove(t)
                return t

        return None