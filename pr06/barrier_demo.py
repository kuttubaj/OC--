import threading
import time
import random

class CustomBarrier:
    def __init__(self, parties):
        self.parties = parties
        self.count = 0
        self.generation = 0
        self.mutex = threading.Lock()
        self.cond = threading.Condition(self.mutex)

    def wait(self):
        with self.cond:
            gen = self.generation
            self.count += 1
            if self.count == self.parties:
                # Последний пришедший поток "пробивает" барьер
                self.count = 0
                self.generation += 1
                self.cond.notify_all()
            else:
                # Остальные ждут смены поколения
                while gen == self.generation:
                    self.cond.wait()

barrier = CustomBarrier(4)

def worker(thread_id):
    for phase in range(1, 4):
        time.sleep(random.uniform(0.1, 0.3))
        print(f"Поток {thread_id} завершил фазу {phase}")
        barrier.wait()
        if thread_id == 1:
            print(f"--- Фаза {phase} пройдена всеми ---")
        barrier.wait() # Синхронизация вывода

if __name__ == '__main__':
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(1, 5)]
    for t in threads: t.start()
    for t in threads: t.join()