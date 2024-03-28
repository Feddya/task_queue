from unittest import TestCase
from TaskQueue import TaskQueue, Resources, Task, DuplicateIdException, DictQueue


class TestTaskQueueSimpleChecksList(TestCase):

    def setUp(self) -> None:
        self.q = TaskQueue()

    def test_get_task_from_empty_q(self):
        r = Resources(1, 1, 1)
        ret = self.q.get_task(r)
        self.assertEqual(ret, None, "empty queue should return none")

    def test_add_task_simple(self):
        t = Task(1, 1, Resources(1, 1, 1), "content", "result")
        try:
            self.q.add_task(t)
        except:
            self.fail("should not throw exception")

    def test_add_task_duplicate_id(self):
        t = Task(1, 1, Resources(1, 1, 1), "content", "result")
        self.q.add_task(t)

        self.assertRaises(DuplicateIdException, self.q.add_task, t)


class TestTaskQueueSimpleChecksDict(TestTaskQueueSimpleChecksList):
    def setUp(self) -> None:
        self.q = TaskQueue(DictQueue())
