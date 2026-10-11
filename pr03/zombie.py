import os
import sys
import time

pid = os.fork()
if pid == 0:
    # Ребенок сразу завершается
    sys.exit(0)
else:
    print(f"[Родитель {os.getpid()}] Ребенок {pid} завершился, но я не вызываю wait().")
    print(f"Процесс {pid} перешел в состояние 'Z' (Zombie).")
    time.sleep(20) # Родитель спит