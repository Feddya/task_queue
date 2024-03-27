from unittest import TestCase
from TaskQueue import TaskQueue, Resources, Task, DuplicateIdException


class TestTaskQueue_simpleChecks(TestCase):

    def test_fail_to_find_task(self):
        q = TaskQueue()
        t = Task(1,1, Resources(100, 100, 100), "content", "result")
        q.add_task(t)

        try:
            self.assertEqual(len(q.queue), 1, "task should be added correctly")

            r = q.get_task(Resources(1,1,1))
            self.assertIsNone(r, "should return None since there is no matching task in queue")
            self.assertEqual(len(q.queue), 1, "task should not be removed")
        except:
            self.fail("should not throw exceptions")


    def test_find_simple(self):
        q = TaskQueue()
        t = Task(1,1, Resources(1, 1, 1), "content", "result")
        q.add_task(t)

        try:
            self.assertEqual(len(q.queue), 1, "task should be added correctly")

            r = q.get_task(Resources(1,1,1))
            self.assertEqual(r, t, "should return previously added task")
            self.assertEqual(len(q.queue), 0, "task should be removed")
        except:
            self.fail("should not throw exceptions")


    def test_find_multiple_priorities(self):
        q = TaskQueue()
        t1 = Task(1, 1, Resources(1, 1, 1), "content", "result")
        t2 = Task(2, 10, Resources(1, 1, 1), "content", "result")
        q.add_task(t1)
        q.add_task(t2)

        try:
            self.assertEqual(len(q.queue), 2, "tasks should be added correctly")

            r = q.get_task(Resources(1,1,1))
            self.assertEqual(r, t2, "should return task with highest priority")
            self.assertEqual(len(q.queue), 1, "task should be removed")
        except:
            self.fail("should not throw exceptions")

    def test_negative_priority(self):
        q = TaskQueue()
        t1 = Task(1, -1, Resources(1, 1, 1), "content", "result")
        t2 = Task(2, 10, Resources(1, 1, 1), "content", "result")
        q.add_task(t1)
        q.add_task(t2)

        try:
            self.assertEqual(len(q.queue), 2, "tasks should be added correctly")

            r = q.get_task(Resources(1,1,1))
            self.assertEqual(r, t2, "should return task with highest priority")
            self.assertEqual(len(q.queue), 1, "task should be removed")

            r = q.get_task(Resources(1,1,1))
            self.assertEqual(r, t1, "should return task with negative priority")
            self.assertEqual(len(q.queue), 0, "task should be removed")

        except:
            self.fail("should not throw exceptions")
