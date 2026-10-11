import os

def create_files():
    # Данные из учебника Silberschatz (§8.6.3)
    b1 = "Available: 3 3 2\nMax:\n0 7 5 3\n1 3 2 2\n2 9 0 2\n3 2 2 2\n4 4 3 3\nAllocation:\n0 0 1 0\n1 2 0 0\n2 3 0 2\n3 2 1 1\n4 0 0 2\n"
    b2 = b1.replace("Available: 3 3 2", "Available: 0 1 0")
    if not os.path.exists("bank1.txt"): open("bank1.txt", "w").write(b1)
    if not os.path.exists("bank2.txt"): open("bank2.txt", "w").write(b2)

def parse_file(filename):
    lines = open(filename).read().strip().split('\n')
    available = list(map(int, lines[0].split(':')[1].split()))
    max_mat, alloc_mat = [], []
    idx = 2
    while lines[idx] != "Allocation:":
        max_mat.append(list(map(int, lines[idx].split()[1:])))
        idx += 1
    idx += 1
    while idx < len(lines):
        alloc_mat.append(list(map(int, lines[idx].split()[1:])))
        idx += 1
    return available, max_mat, alloc_mat

def check_safety(available, max_mat, alloc_mat):
    n_procs, n_res = len(max_mat), len(available)
    need_mat = [[max_mat[i][j] - alloc_mat[i][j] for j in range(n_res)] for i in range(n_procs)]
    
    work = available[:]
    finish = [False] * n_procs
    safe_seq = []

    while len(safe_seq) < n_procs:
        allocated_in_this_round = False
        for i in range(n_procs):
            if not finish[i] and all(need_mat[i][j] <= work[j] for j in range(n_res)):
                for j in range(n_res):
                    work[j] += alloc_mat[i][j]
                finish[i] = True
                safe_seq.append(f"P{i}")
                allocated_in_this_round = True
        
        if not allocated_in_this_round:
            return False, []
            
    return True, safe_seq

if __name__ == "__main__":
    create_files()
    for fname in ["bank1.txt", "bank2.txt"]:
        avail, mx, alloc = parse_file(fname)
        is_safe, seq = check_safety(avail, mx, alloc)
        if is_safe:
            print(f"[{fname}] Состояние: БЕЗОПАСНО. Последовательность: {', '.join(seq)}")
        else:
            print(f"[{fname}] Состояние: НЕБЕЗОПАСНО (UNSAFE - возможен Deadlock).")