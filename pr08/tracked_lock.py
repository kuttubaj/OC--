import threading
import time

class DeadlockException(Exception): pass

class TrackedLock:
    wait_for_graph = {} # Кто (поток) ждет кого (поток)
    graph_lock = threading.Lock()
    
    def __init__(self, name):
        self.name = name
        self._lock = threading.Lock()
        self.owner = None

    def _check_cycle(self, start_node):
        visited = set()
        current = start_node
        while current in self.wait_for_graph:
            visited.add(current)
            current = self.wait_for_graph[current]
            if current in visited:
                return True
        return False

    def acquire(self):
        me = threading.current_thread().name
        with TrackedLock.graph_lock:
            if self.owner is not None and self.owner != me:
                TrackedLock.wait_for_graph[me] = self.owner
                if self._check_cycle(me):
                    del TrackedLock.wait_for_graph[me]
                    raise DeadlockException(f"Обнаружен Deadlock! Поток {me} попытался захватить {self.name}.")
                    
        self._lock.acquire()
        
        with TrackedLock.graph_lock:
            if me in TrackedLock.wait_for_graph:
                del TrackedLock.wait_for_graph[me]
            self.owner = me

    def release(self):
        with TrackedLock.graph_lock:
            self.owner = None
        self._lock.release()

lock_a = TrackedLock("LockA")
lock_b = TrackedLock("LockB")

def thread_1():
    try:
        lock_a.acquire()
        time.sleep(0.1)
        lock_b.acquire()
        lock_b.release()
        lock_a.release()
    except Exception as e:
        print(f"[Т1] {e}")

def thread_2():
    try:
        lock_b.acquire()
        time.sleep(0.1)
        lock_a.acquire()
        lock_a.release()
        lock_b.release()
    except Exception as e:
        print(f"[Т2] {e}")

if __name__ == "__main__":
    t1 = threading.Thread(target=thread_1, name="Thread-1")
    t2 = threading.Thread(target=thread_2, name="Thread-2")
    t1.start(); t2.start()
    t1.join(); t2.join()