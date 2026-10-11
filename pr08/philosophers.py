import threading
import time

N = 5
meals = [0] * N
running = True

def philosopher(idx, left_fork, right_fork, mode, waiter_sem=None):
    global meals
    while running:
        if mode == "limit" and waiter_sem:
            waiter_sem.acquire()

        # Захват вилок
        if mode == "hierarchy":
            first, second = min(left_fork, right_fork, key=id), max(left_fork, right_fork, key=id)
            first.acquire(); second.acquire()
        else: # naive или limit
            left_fork.acquire(); time.sleep(0.001); right_fork.acquire()

        # Еда
        meals[idx] += 1
        
        # Освобождение
        right_fork.release(); left_fork.release()
        
        if mode == "limit" and waiter_sem:
            waiter_sem.release()
        time.sleep(0.001)

def run_simulation(mode, duration=2):
    global meals, running
    meals = [0] * N
    running = True
    forks = [threading.Lock() for _ in range(N)]
    waiter = threading.Semaphore(N - 1) if mode == "limit" else None
    
    threads = []
    for i in range(N):
        l_fork, r_fork = forks[i], forks[(i + 1) % N]
        t = threading.Thread(target=philosopher, args=(i, l_fork, r_fork, mode, waiter))
        threads.append(t)
        t.start()
        
    time.sleep(duration)
    running = False
    # Если deadlock в наивном режиме - скрипт зависнет, это ожидаемо!
    # Поэтому для наивного режима мы не делаем join
    if mode != "naive":
        for t in threads: t.join()
    print(f"Режим '{mode}': Съедено порций: {meals} (Всего: {sum(meals)})")

if __name__ == "__main__":
    print("1. Иерархия (нумерация ресурсов):")
    run_simulation("hierarchy")
    
    print("\n2. Ограничение мест (Семафор N-1):")
    run_simulation("limit")
    
    print("\n3. Наивный (Deadlock). Программа зависнет, нажмите Ctrl+C...")
    run_simulation("naive")