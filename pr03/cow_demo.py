import os
import sys

def get_rss():
    with open("/proc/self/status") as f:
        for line in f:
            if line.startswith("VmRSS"):
                return line.split()[1] + " KB"
    return "0 KB"

# Создаем большой список (выделяем память)
big_list = [0] * (10**7)

pid = os.fork()
if pid == 0:
    print(f"[Ребенок] RSS до изменения списка:   {get_rss()}")
    # Изменяем список. Только сейчас Linux физически скопирует память! (Copy-on-Write)
    for i in range(10**6):
        big_list[i] = 1
    print(f"[Ребенок] RSS после изменения списка: {get_rss()}")
    sys.exit(0)
else:
    os.wait()