from unittest import TestCase
from TaskQueue import TaskQueue, Resources, Task, DuplicateIdException, DictQueue


class TestTaskQueueWorkChecksList(TestCase):

    def setUp(self) -> None:
        self.q = TaskQueue()

    def test_fail_to_find_task(self):
        t = Task(1,1, Resources(100, 100, 100), "content", "result")
        self.q.add_task(t)

        try:
            self.assertEqual(self.q.get_queue_length(), 1, "task should be added correctly")

            r = self.q.get_task(Resources(1,1,1))
            self.assertIsNone(r, "should return None since there is no matching task in queue")
            self.assertEqual(self.q.get_queue_length(), 1, "task should not be removed")
        except:
            self.fail("should not throw exceptions")


    def test_find_simple(self):
        t = Task(1,1, Resources(1, 1, 1), "content", "result")
        self.q.add_task(t)

        try:
            self.assertEqual(self.q.get_queue_length(), 1, "task should be added correctly")

            r = self.q.get_task(Resources(1,1,1))
            self.assertEqual(r, t, "should return previously added task")
            self.assertEqual(self.q.get_queue_length(), 0, "task should be removed")
        except:
            self.fail("should not throw exceptions")


    def test_find_multiple_priorities(self):
        t1 = Task(1, 1, Resources(1, 1, 1), "content", "result")
        t2 = Task(2, 10, Resources(1, 1, 1), "content", "result")
        self.q.add_task(t1)
        self.q.add_task(t2)

        try:
            self.assertEqual(self.q.get_queue_length(), 2, "tasks should be added correctly")

            r = self.q.get_task(Resources(1,1,1))
            self.assertEqual(r, t2, "should return task with highest priority")
            self.assertEqual(self.q.get_queue_length(), 1, "task should be removed")
        except:
            self.fail("should not throw exceptions")

    def test_negative_priority(self):
        t1 = Task(1, -1, Resources(1, 1, 1), "content", "result")
        t2 = Task(2, 10, Resources(1, 1, 1), "content", "result")
        self.q.add_task(t1)
        self.q.add_task(t2)

        try:
            self.assertEqual(self.q.get_queue_length(), 2, "tasks should be added correctly")

            r = self.q.get_task(Resources(1,1,1))
            self.assertEqual(r, t2, "should return task with highest priority")
            self.assertEqual(self.q.get_queue_length(), 1, "task should be removed")

            r = self.q.get_task(Resources(1,1,1))
            self.assertEqual(r, t1, "should return task with negative priority")
            self.assertEqual(self.q.get_queue_length(), 0, "task should be removed")

        except:
            self.fail("should not throw exceptions")

    def test_multiple_same_priority(self):
        t1 = Task(1, 1, Resources(1, 1, 1), "content1", "result1")
        t2 = Task(2, 1, Resources(1, 1, 1), "content2", "result2")
        t3 = Task(3, -10, Resources(1, 1, 1), "content3", "result3")
        self.q.add_task(t1)
        self.q.add_task(t2)
        self.q.add_task(t3)

        try:
            self.assertEqual(self.q.get_queue_length(), 3, "tasks should be added correctly")

            r = self.q.get_task(Resources(1,1,1))
            self.assertNotEqual(r, t3, "should return any found task with priority == 1, so not t3")
            self.assertEqual(self.q.get_queue_length(), 2, "task should be removed")

            r = self.q.get_task(Resources(1,1,1))
            self.assertNotEqual(r, t3, "should return another task with priority == 1")
            self.assertEqual(self.q.get_queue_length(), 1, "task should be removed")

        except:
            self.fail("should not throw exceptions")


# running the same tests for different implementation
class TestTaskQueueWorkChecksDict(TestTaskQueueWorkChecksList):
    def setUp(self) -> None:
        self.q = TaskQueue(DictQueue())