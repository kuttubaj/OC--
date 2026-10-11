import sys

if len(sys.argv) < 2:
    print("Использование: python3 hello.py <файл>")
    sys.exit(1)

filename = sys.argv[1]
with open(filename, 'rb') as f:
    data = f.read()
    print(f"Размер файла: {len(data)} байт")