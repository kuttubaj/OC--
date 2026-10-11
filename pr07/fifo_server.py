import os

REQ_FIFO = "/tmp/calc_req"
RES_FIFO = "/tmp/calc_res"

# Очистка старых каналов, если они остались
for f in [REQ_FIFO, RES_FIFO]:
    if os.path.exists(f):
        os.unlink(f)

# Создание именованных каналов
os.mkfifo(REQ_FIFO)
os.mkfifo(RES_FIFO)

print("FIFO Сервер запущен. Ожидание выражений...")
try:
    while True:
        # Сервер блокируется (висит), ожидая записи от клиента
        with open(REQ_FIFO, 'r') as req:
            expr = req.read().strip()
            if not expr:
                continue
            
            print(f"Получено: {expr}")
            try:
                # ВНИМАНИЕ: eval() используется только в учебных целях!
                result = str(eval(expr))
            except Exception as e:
                result = f"Ошибка: {e}"
                
        # Отправка результата
        with open(RES_FIFO, 'w') as res:
            res.write(result)
except KeyboardInterrupt:
    print("\nЗавершение работы сервера...")
finally:
    # Требование ТЗ: после завершения не остается FIFO
    for f in [REQ_FIFO, RES_FIFO]:
        if os.path.exists(f):
            os.unlink(f)