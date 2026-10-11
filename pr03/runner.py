import os
import sys
import time

if len(sys.argv) < 3:
    print("Использование: python3 runner.py <N> <команда>")
    sys.exit(1)

n = int(sys.argv[1])
cmd = sys.argv[2:]
start_times = {}

# Создаем N процессов
for _ in range(n):
    pid = os.fork()
    if pid == 0:
        # Ветка ребенка: замещаем себя новой командой
        os.execvp(cmd[0], cmd)
    else:
        # Ветка родителя: запоминаем время старта
        start_times[pid] = time.time()

# Родитель ждет завершения всех детей
for _ in range(n):
    pid, status = os.wait()
    elapsed = time.time() - start_times[pid]
    # Вытаскиваем код возврата из статуса
    exit_code = status >> 8
    print(f"Процесс {pid} завершился с кодом {exit_code} за {elapsed:.4f} сек")