#!/bin/bash

# Проверка наличия минимального числа аргументов
if [ "$#" -lt 2 ]; then
    echo "Использование: $0 <каталог> <уровень_ошибки> [--top N]"
    echo "Пример: $0 data ERROR --top 5"
    exit 1
fi

DIR=$1
LEVEL=$2
TOP_N=""

# Проверка флага --top N
if [ "$3" = "--top" ] && [ -n "$4" ]; then
    TOP_N=$4
fi

# Проверка существования каталога
if [ ! -d "$DIR" ]; then
    echo "Ошибка: каталог '$DIR' не существует."
    exit 1
fi

echo "Таблица: Модуль -> Число сообщений ($LEVEL)"
echo "----------------------------------------"

# Парсинг логов: ищем уровень, вытаскиваем имя модуля, считаем и сортируем
if [ -z "$TOP_N" ]; then
    grep -h "$LEVEL" "$DIR"/*.log 2>/dev/null | grep -o 'module=[^ ]*' | cut -d= -f2 | sort | uniq -c | sort -nr | awk '{print $2 " -> " $1}'
else
    grep -h "$LEVEL" "$DIR"/*.log 2>/dev/null | grep -o 'module=[^ ]*' | cut -d= -f2 | sort | uniq -c | sort -nr | head -n "$TOP_N" | awk '{print $2 " -> " $1}'
fi