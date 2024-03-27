# Initial task description
Task description:
* Requires a task queue with priorities and resource limits.
* Each task has a priority and the required amount of resources to process it.
* Publishers create tasks with specified resource limits, and put them in a task queue.
* Consumer receives the highest priority task that satisfies available resources.
* The queue is expected to contain thousands of tasks.
* Write a unit test to demonstrate the operation of the queue.

```python
from dataclasses import dataclass


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str


class TaskQueue:
    def add_task(self):
        pass

    def get_task(self, available_resources: Resources) -> Task:
        pass
```

# My additions to task description
- add_task function should add externally provided task, so, it should look like ```def add_task(self, task: Task)```
- After task is returned in get_task function - it removed from queue.
- Task.id field is unique.
- If we have multiple the same tasks matching criterion - first found task will be returned.
- Highest priority (task will be returned first) means higher integer value.
- Added queue length getter function 