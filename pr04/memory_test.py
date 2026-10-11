import threading
import multiprocessing
import time

# Глобальный список для тестирования
shared_memory = ["Начало"]

def thread_worker():
    shared_memory.append("Изменено потоком")

def process_worker(shared_list):
    shared_list.append("Изменено процессом")
    # Процесс меняет только свою локальную копию памяти

if __name__ == '__main__':
    print(f"Исходный список: {shared_memory}")
    
    # 1. Тест потоков
    t = threading.Thread(target=thread_worker)
    t.start()
    t.join()
    print(f"После потока: {shared_memory} (Память общая!)")
    
    # 2. Тест процессов
    shared_memory = ["Начало"] # Сброс
    p = multiprocessing.Process(target=process_worker, args=(shared_memory,))
    p.start()
    p.join()
    print(f"После процесса: {shared_memory} (Память изолирована!)") 