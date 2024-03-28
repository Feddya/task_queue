from dataclasses import dataclass
from abc import ABC, abstractmethod
from collections import defaultdict

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

        sq = sorted(self._queue, key=lambda t: t.priority, reverse=True)
        for t in sq:
            if t.resources <= available_resources:
                self._queue.remove(t)
                return t

        return None


class DictQueue(QueueImplementationBase):

    def __init__(self):

        # id -> Task
        self._queue = {}

        # priority -> list of task id
        self._priority_dict = defaultdict(list)

        # ram -> list of task id
        self._ram_dict = defaultdict(list)

        # cpu -> list of task id
        self._cpu_dict = defaultdict(list)

        # gpu -> list of task id
        self._gpu_dict = defaultdict(list)

    def get_queue_length(self) -> int:
        return len(self._queue)

    def add_task(self, task: Task) -> None:

        self._queue[task.id] = task

        self._priority_dict[task.priority].append(task.id)
        self._ram_dict[task.resources.ram].append(task.id)
        self._cpu_dict[task.resources.cpu_cores].append(task.id)
        self._gpu_dict[task.resources.gpu_count].append(task.id)

    def is_task_already_added(self, task: Task) -> bool:
        return task.id in self._queue

    def get_task(self, available_resources: Resources) -> [Task, None]:

        ram_set = self._collect_matching_to_set(self._ram_dict, available_resources.ram)

        cpu_set = self._collect_matching_to_set(self._cpu_dict, available_resources.cpu_cores)

        gpu_set = self._collect_matching_to_set(self._gpu_dict, available_resources.gpu_count)

        all_matching = set.intersection(ram_set, cpu_set, gpu_set)
        if not all_matching:
            return None

        # getting task with highest priority from all matching
        max_priority = float("-inf")
        ret_id = None
        ret_task = None
        for i in all_matching:
            task = self._queue[i]
            if task.priority > max_priority:
                max_priority = task.priority
                ret_id = i
                ret_task = task

        # remove item from collections
        self._remove_from_dict_by_value(self._ram_dict, ret_task.resources.ram, ret_id)
        self._remove_from_dict_by_value(self._cpu_dict, ret_task.resources.cpu_cores, ret_id)
        self._remove_from_dict_by_value(self._gpu_dict, ret_task.resources.gpu_count, ret_id)
        del self._queue[ret_id]

        return ret_task

    @staticmethod
    def _collect_matching_to_set(collection: dict, value: int) -> set:

        ret = set()
        for item in collection.keys():
            if item <= value:
                ret.update(collection[item])

        return ret

    @staticmethod
    def _remove_from_dict_by_value(collection: dict, key:int, value: int):
        lst = collection[key]
        lst.remove(value)


class TaskQueue:

    def __init__(self, queueImpl=None):
        if not queueImpl:
            self._queue = ListQueue()
        else:
            self._queue = queueImpl

    def get_queue_length(self) -> int:
        return self._queue.get_queue_length()

    def add_task(self, task: Task) -> None:

        if self._queue.is_task_already_added(task):
            raise DuplicateIdException(f"duplicate id {task.id} found in add_task")

        self._queue.add_task(task)

    def get_task(self, available_resources: Resources) -> [Task, None]:
        return self._queue.get_task(available_resources)