import os
import argparse
import matplotlib.pyplot as plt

# --- 1. АВТОГЕНЕРАЦИЯ ДАННЫХ ---
def ensure_datasets():
    os.makedirs('data', exist_ok=True)
    datasets = {
        'set1.txt': "P1 0 8 1\nP2 1 4 1\nP3 2 9 1\nP4 3 5 1\n",
        'set2.txt': "\n".join([f"P{i} {i%3} {10 + (i%5)*2} {i%4 + 1}" for i in range(1, 21)]),
        'starvation_set.txt': "P1 0 20 4\nP2 1 5 1\nP3 2 5 1\nP4 3 5 1\nP5 4 5 1\nP6 5 5 1\n"
    }
    for name, content in datasets.items():
        path = os.path.join('data', name)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)

# --- 2. ЛОГИКА СИМУЛЯТОРА ---
class Process:
    def __init__(self, pid, arr, burst, prio):
        self.pid = pid
        self.arr = arr
        self.burst = burst
        self.prio = prio
        self.rem = burst
        self.current_prio = prio # для старения
        self.start_time = -1
        self.finish_time = 0

def simulate(processes_data, algo, quantum=1):
    procs = [Process(*p) for p in processes_data]
    procs.sort(key=lambda x: x.arr)
    
    t, completed = 0, 0
    ready_queue = []
    current = None
    current_q_used = 0
    prev_pid = None
    context_switches = 0
    wait_times_tracking = {p.pid: 0 for p in procs}

    while completed < len(procs):
        # 1. Прибытие новых процессов
        arriving = [p for p in procs if p.arr == t]
        ready_queue.extend(arriving)

        # 2. Обработка текущего процесса (завершение или вытеснение)
        if current:
            if current.rem == 0:
                current.finish_time = t
                completed += 1
                current = None
            elif algo == 'rr' and current_q_used == quantum:
                # В RR вытесненный процесс встает ПОСЛЕ только что прибывших (строго по ТЗ)
                ready_queue.append(current)
                current = None
            elif algo in ['srtf', 'priority', 'priority_aging']:
                # Проверка на вытеснение
                best = None
                if algo == 'srtf':
                    best = min(ready_queue, key=lambda x: (x.rem, x.arr), default=None)
                    if best and best.rem < current.rem:
                        ready_queue.append(current)
                        current = None
                elif algo == 'priority':
                    best = min(ready_queue, key=lambda x: (x.prio, x.arr), default=None)
                    if best and best.prio < current.prio:
                        ready_queue.append(current)
                        current = None
                elif algo == 'priority_aging':
                    best = min(ready_queue, key=lambda x: (x.current_prio, x.arr), default=None)
                    if best and best.current_prio < current.current_prio:
                        ready_queue.append(current)
                        current = None

        # 3. Выбор следующего процесса
        if not current and ready_queue:
            if algo in ['fcfs', 'rr']:
                current = ready_queue.pop(0)
            elif algo == 'sjf':
                current = min(ready_queue, key=lambda x: (x.burst, x.arr))
                ready_queue.remove(current)
            elif algo == 'srtf':
                current = min(ready_queue, key=lambda x: (x.rem, x.arr))
                ready_queue.remove(current)
            elif algo == 'priority':
                current = min(ready_queue, key=lambda x: (x.prio, x.arr))
                ready_queue.remove(current)
            elif algo == 'priority_aging':
                current = min(ready_queue, key=lambda x: (x.current_prio, x.arr))
                ready_queue.remove(current)
            
            current_q_used = 0
            if current.start_time == -1:
                current.start_time = t
            
            if current.pid != prev_pid:
                context_switches += 1
                prev_pid = current.pid

        # 4. Выполнение и старение
        if current:
            current.rem -= 1
            current_q_used += 1

        if algo == 'priority_aging':
            for p in ready_queue:
                wait_times_tracking[p.pid] += 1
                if wait_times_tracking[p.pid] % 5 == 0:
                    p.current_prio -= 1 # Увеличиваем приоритет (число меньше)

        t += 1

    # Подсчет метрик
    total_wait = sum(p.finish_time - p.arr - p.burst for p in procs)
    total_turn = sum(p.finish_time - p.arr for p in procs)
    total_resp = sum(p.start_time - p.arr for p in procs)
    
    return total_wait / len(procs), total_turn / len(procs), total_resp / len(procs), context_switches

# --- 3. ИНТЕРФЕЙС И ГРАФИКИ ---
def load_data(filename):
    data = []
    with open(os.path.join('data', filename), 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.split()
            data.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
    return data

def plot_rr_tradeoff():
    data = load_data('set2.txt')
    quantums = list(range(1, 11))
    waits, switches = [], []
    for q in quantums:
        w, _, _, s = simulate(data, 'rr', quantum=q)
        waits.append(w)
        switches.append(s)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.set_xlabel('Квант времени (Quantum)')
    ax1.set_ylabel('Среднее время ожидания', color='tab:blue')
    ax1.plot(quantums, waits, marker='o', color='tab:blue', label='Ожидание')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Число переключений контекста', color='tab:red')
    ax2.plot(quantums, switches, marker='x', linestyle='dashed', color='tab:red', label='Переключения')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    plt.title('RR: Компромисс между ожиданием и накладными расходами (set2.txt)')
    plt.tight_layout()
    plt.savefig('rr_tradeoff.png')
    print("[+] График успешно сохранен как rr_tradeoff.png")

if __name__ == '__main__':
    ensure_datasets()
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default='set1.txt')
    parser.add_argument('--algo', choices=['fcfs', 'sjf', 'srtf', 'priority', 'priority_aging', 'rr'])
    parser.add_argument('--quantum', type=int, default=3)
    parser.add_argument('--plot', action='store_true')
    args = parser.parse_args()

    if args.plot:
        plot_rr_tradeoff()
    elif args.algo:
        data = load_data(args.file)
        wait, turn, resp, cs = simulate(data, args.algo, args.quantum)
        print(f"--- Результаты {args.algo.upper()} для {args.file} ---")
        print(f"Среднее ожидание: {wait:.2f}")
        print(f"Средний оборот:   {turn:.2f}")
        print(f"Средний отклик:   {resp:.2f}")
    else:
        print("Используйте флаг --plot для генерации графика или укажите --algo")