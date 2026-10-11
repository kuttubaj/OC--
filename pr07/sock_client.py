import socket
import sys

SOCK_FILE = "/tmp/calc_sock"
expr = sys.argv[1] if len(sys.argv) > 1 else "10 * 10"

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCK_FILE)
client.send(expr.encode())

result = client.recv(1024).decode()
print(f"Результат от сервера: {result}")
client.close()