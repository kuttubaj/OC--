import socket
import os
import multiprocessing

SOCK_FILE = "/tmp/calc_sock"

if os.path.exists(SOCK_FILE):
    os.unlink(SOCK_FILE)

def handle_client(conn):
    try:
        data = conn.recv(1024).decode().strip()
        print(f"[Процесс {os.getpid()}] Вычисляет: {data}")
        result = str(eval(data))
        conn.send(result.encode())
    except Exception as e:
        conn.send(f"Ошибка: {e}".encode())
    finally:
        conn.close()

if __name__ == '__main__':
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCK_FILE)
    server.listen(5)
    print("Unix-сокет Сервер запущен...")
    
    try:
        while True:
            conn, _ = server.accept()
            # На каждого клиента создается свой процесс
            p = multiprocessing.Process(target=handle_client, args=(conn,))
            p.start()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        server.close()
        if os.path.exists(SOCK_FILE):
            os.unlink(SOCK_FILE)