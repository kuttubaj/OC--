import threading

BUFFER_SIZE = 5
TOTAL_ITEMS = 1000

buffer = [None] * BUFFER_SIZE
in_idx = 0
out_idx = 0
count = 0  # Число элементов в буфере

mutex = threading.Lock()
cond = threading.Condition(mutex)

produced_count = 0
consumed_count = 0
consumed_set = set()

def producer(items_to_produce):
    global in_idx, count, produced_count
    for _ in range(items_to_produce):
        with cond:
            # ПРАВИЛЬНО: while (предотвращает потерянное пробуждение)
            while count == BUFFER_SIZE:
                cond.wait()
            
            item = f"Item-{produced_count}"
            buffer[in_idx] = item
            in_idx = (in_idx + 1) % BUFFER_SIZE
            count += 1
            produced_count += 1
            
            cond.notify_all()

def consumer():
    global out_idx, count, consumed_count
    while True:
        with cond:
            while count == 0:
                if consumed_count >= TOTAL_ITEMS:
                    return
                cond.wait()
                
            if consumed_count >= TOTAL_ITEMS:
                return
                
            item = buffer[out_idx]
            out_idx = (out_idx + 1) % BUFFER_SIZE
            count -= 1
            consumed_count += 1
            
            if item in consumed_set:
                print(f"[ОШИБКА] Дубликат: {item}")
            consumed_set.add(item)
            
            cond.notify_all()

if __name__ == '__main__':
    producers = [threading.Thread(target=producer, args=(334,)),
                 threading.Thread(target=producer, args=(333,)),
                 threading.Thread(target=producer, args=(333,))]
    consumers = [threading.Thread(target=consumer) for _ in range(2)]

    for t in producers + consumers: t.start()
    for t in consumers:
        with cond:
            cond.notify_all() # Будим потребителей для завершения
            
    for t in producers + consumers: t.join()
    print(f"CondVar: Потреблено элементов: {consumed_count}")