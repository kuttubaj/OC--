import threading
import time

BUFFER_SIZE = 5
TOTAL_ITEMS = 1000

buffer = [None] * BUFFER_SIZE
in_idx = 0
out_idx = 0

# Примитивы синхронизации
mutex = threading.Lock()
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

# Глобальные счетчики для проверки инвариантов
produced_count = 0
consumed_count = 0
consumed_set = set()
buffer_count = 0  # Текущее число элементов в буфере
invariant_lock = threading.Lock()

def producer(items_to_produce):
    global in_idx, produced_count, buffer_count
    for _ in range(items_to_produce):
        empty.acquire()
        mutex.acquire()
        
        # Критическая секция (Производство)
        item = f"Item-{produced_count}"
        buffer[in_idx] = item
        in_idx = (in_idx + 1) % BUFFER_SIZE
        produced_count += 1
        buffer_count += 1
        
        # Проверка на переполнение
        if buffer_count > BUFFER_SIZE:
            print(f"[ОШИБКА] Переполнение буфера! Размер: {buffer_count}")
            
        mutex.release()
        full.release()

def consumer():
    global out_idx, consumed_count, buffer_count
    while True:
        with invariant_lock:
            if consumed_count >= TOTAL_ITEMS:
                break
                
        full.acquire()
        mutex.acquire()
        
        # Двойная проверка после захвата блокировки
        if consumed_count >= TOTAL_ITEMS:
            mutex.release()
            full.release()
            break
            
        # Критическая секция (Потребление)
        item = buffer[out_idx]
        buffer[out_idx] = None
        out_idx = (out_idx + 1) % BUFFER_SIZE
        buffer_count -= 1
        consumed_count += 1
        
        mutex.release()
        empty.release()
        
        # Проверка на дубликаты
        with invariant_lock:
            if item in consumed_set:
                print(f"[ОШИБКА] Элемент {item} потреблен дважды!")
            consumed_set.add(item)

if __name__ == '__main__':
    # 3 производителя (334 + 333 + 333 = 1000), 2 потребителя
    producers = [threading.Thread(target=producer, args=(334,)),
                 threading.Thread(target=producer, args=(333,)),
                 threading.Thread(target=producer, args=(333,))]
    consumers = [threading.Thread(target=consumer) for _ in range(2)]

    for t in producers + consumers: t.start()
    for t in producers + consumers: t.join()

    print(f"Семафоры: Потреблено элементов: {consumed_count} (Ожидалось {TOTAL_ITEMS})")
    print(f"Ошибок дубликатов: {TOTAL_ITEMS - len(consumed_set)}")