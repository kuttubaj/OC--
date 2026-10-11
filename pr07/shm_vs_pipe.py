import multiprocessing
from multiprocessing import shared_memory
import time

DATA_SIZE = 10_000_000 * 8 # ~80 MB данных
dummy_data = b'1' * DATA_SIZE

def pipe_receiver(conn):
    data = conn.recv()
    conn.close()

def shm_receiver(shm_name, event):
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    data = existing_shm.buf[:]
    existing_shm.close()
    event.set()

if __name__ == '__main__':
    print("Генерация данных (80 MB)...")
    
    # --- 1. Тест Pipe ---
    parent_conn, child_conn = multiprocessing.Pipe()
    p_pipe = multiprocessing.Process(target=pipe_receiver, args=(child_conn,))
    
    start = time.time()
    p_pipe.start()
    parent_conn.send(dummy_data)
    p_pipe.join()
    pipe_time = time.time() - start
    
    # --- 2. Тест Shared Memory ---
    shm = shared_memory.SharedMemory(create=True, size=DATA_SIZE)
    shm.buf[:] = dummy_data
    event = multiprocessing.Event()
    p_shm = multiprocessing.Process(target=shm_receiver, args=(shm.name, event))
    
    start = time.time()
    p_shm.start()
    event.wait()
    p_shm.join()
    shm_time = time.time() - start
    
    # Очистка
    shm.close()
    shm.unlink()

    print(f"Время передачи через Pipe:          {pipe_time:.4f} сек")
    print(f"Время передачи через Shared Memory: {shm_time:.4f} сек")