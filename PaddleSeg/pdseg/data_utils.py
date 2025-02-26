"""
This code is based on https://github.com/fchollet/keras/blob/master/keras/utils/data_utils.py
"""

import multiprocessing
import time

try:
    import queue
except ImportError:
    import Queue as queue


class GeneratorEnqueuer(object):
    """
    Multiple generators 

    Args:
        generators: 
        wait_time (float): time to sleep in-between calls to `put()`.
    """

    def __init__(self, generators, wait_time=0.05):
        self.wait_time = wait_time
        self._generators = generators
        self._threads = []
        self._stop_events = []
        self.queue = None
        self._manager = None
        self.workers = 1

    def start(self, workers=1, max_queue_size=16):
        """
        Start worker threads which add data from the generator into the queue.

        Args:
            workers (int): number of worker threads
            max_queue_size (int): queue size
                (when full, threads could block on `put()`)
        """

        self.workers = workers

        def data_generator_task(pid):
            """
            Data generator task.
            """

            def task(pid):
                if (self.queue is not None
                        and self.queue.qsize() < max_queue_size):
                    generator_output = next(self._generators[pid])
                    self.queue.put((generator_output))
                else:
                    time.sleep(self.wait_time)

            while not self._stop_events[pid].is_set():
                try:
                    task(pid)
                except Exception:
                    self._stop_events[pid].set()
                    break

        try:
            self._manager = multiprocessing.Manager()
            self.queue = self._manager.Queue(maxsize=max_queue_size)
            for pid in range(self.workers):
                self._stop_events.append(multiprocessing.Event())
                thread = multiprocessing.Process(
                    target=data_generator_task, args=(pid, ))
                thread.daemon = True
                self._threads.append(thread)
                thread.start()
        except:
            self.stop()
            raise

    def is_running(self):
        """
        Returns:
            bool: Whether the worker theads are running.
        """

        # If queue is not empty then still in runing state wait for consumer
        if not self.queue.empty():
            return True

        for pid in range(self.workers):
            if not self._stop_events[pid].is_set():
                return True

        return False

    def stop(self, timeout=None):
        """
        Stops running threads and wait for them to exit, if necessary.
        Should be called by the same thread which called `start()`.

        Args:
            timeout(int|None): maximum time to wait on `thread.join()`.
        """
        if self.is_running():
            for pid in range(self.workers):
                self._stop_events[pid].set()

        for thread in self._threads:
            if thread.is_alive():
                thread.join(timeout)
        if self._manager:
            self._manager.shutdown()

        self._threads = []
        self._stop_events = []
        self.queue = None
