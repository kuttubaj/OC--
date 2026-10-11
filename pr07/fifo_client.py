import sys

REQ_FIFO = "/tmp/calc_req"
RES_FIFO = "/tmp/calc_res"

expr = sys.argv[1] if len(sys.argv) > 1 else "2 + 2"

# Отправляем выражение
with open(REQ_FIFO, 'w') as req:
    req.write(expr)

# Читаем результат
with open(RES_FIFO, 'r') as res:
    print(f"Результат вычисления '{expr}': {res.read().strip()}")