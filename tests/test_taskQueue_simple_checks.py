from unittest import TestCase
from TaskQueue import TaskQueue, Resources, Task, DuplicateIdException


class TestTaskQueueSimpleChecks(TestCase):

    def test_get_task_from_empty_q(self):
        q = TaskQueue()
        r = Resources(1,1,1)
        ret = q.get_task(r)
        self.assertEqual(ret, None, "empty queue should return none")

    def test_add_task_simple(self):
        q = TaskQueue()
        t = Task(1, 1, Resources(1,1,1), "content", "result")
        try:
            q.add_task(t)
        except:
            self.fail("should not throw exception")

    def test_add_task_duplicate_id(self):

        q = TaskQueue()

        t = Task(1, 1, Resources(1,1,1), "content", "result")
        q.add_task(t)

        self.assertRaises(DuplicateIdException, q.add_task, t)

