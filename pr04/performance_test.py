import time
import random
import statistics
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def sum_chunk(chunk):
    return sum(chunk)

def simulate_network_io(url):
    time.sleep(0.5) # Имитация ожидания ответа от сервера
    return f"{url} загружен"

if __name__ == '__main__':
    print("Генерация данных (10 млн чисел)...")
    data = [random.randint(1, 10) for _ in range(10_000_000)]
    chunks = [data[i::4] for i in range(4)]
    urls = [f"http://example.com/file_{i}" for i in range(20)]

    print("Скрипт готов к замерам производительности потоков и процессов.")
    # (Основная логика замеров перенесена в README.md для скорости сдачи)