import pytest

from proq.queue import ClosedProqQueueError, ProqQueue


class TestProqQueue:
    def test_create_returns_empty_object(self):
        assert ProqQueue().close().collect() == []

    def test_put_get_returns_expected_object(self):
        assert ProqQueue().put(1).get() == 1

    def test_init_and_collect_returns_objects(self):
        assert ProqQueue([1, 2, 3]).close().collect() == [1, 2, 3]

    def test_collect_and_list_return_same_result(self):
        a = ProqQueue([1, 2, 3]).close()
        b = ProqQueue([1, 2, 3]).close()
        assert a.collect() == list(b)

    def test_get_after_close_returns_items_and_then_raises_errors(self):
        queue = ProqQueue([1, 2, 3]).close()
        assert queue.get() == 1
        assert queue.get() == 2
        assert queue.get() == 3
        with pytest.raises(ClosedProqQueueError):
            queue.get()
        with pytest.raises(ClosedProqQueueError):
            queue.get()
