import threading
import queue



# Custom thread pool class
class ThreadPool:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.thread_pool = []
        self.task_queue = queue.Queue()

        # Create and start threads
        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker)
            thread.start()
            self.thread_pool.append(thread)

    def _worker(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                # None is used to signal thread termination
                break
            task()
            self.task_queue.task_done()

    def submit(self, task):
        self.task_queue.put(task)

    def close(self):
        # Add None for each thread to signal termination
        for _ in range(self.num_threads):
            self.task_queue.put(None)

        # Wait for all threads to finish
        for thread in self.thread_pool:
            thread.join()
