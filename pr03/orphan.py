import os
import sys
import time

pid = os.fork()
if pid == 0:
    print(f"[Ребенок {os.getpid()}] Мой родитель: {os.getppid()}")
    time.sleep(2) # Ждем, пока родитель умрет
    print(f"[Ребенок {os.getpid()}] Родитель мертв. Мой новый родитель (усыновитель): {os.getppid()}")
    sys.exit(0)
else:
    print(f"[Родитель {os.getpid()}] Я завершаюсь, бросая ребенка {pid}!")
    sys.exit(0)