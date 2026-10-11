import os

def build_tree():
    processes = {}
    my_uid = os.getuid()

    for pid_dir in os.listdir('/proc'):
        if not pid_dir.isdigit(): continue
        try:
            with open(f'/proc/{pid_dir}/status', 'r') as f:
                lines = f.readlines()
            
            uid = ppid = state = name = rss = ""
            for line in lines:
                if line.startswith('Name:'): name = line.split()[1]
                elif line.startswith('State:'): state = line.split()[1]
                elif line.startswith('PPid:'): ppid = int(line.split()[1])
                elif line.startswith('Uid:'): uid = int(line.split()[1])
                elif line.startswith('VmRSS:'): rss = line.split()[1] + " KB"
            
            if uid == my_uid:
                processes[int(pid_dir)] = {'ppid': ppid, 'state': state, 'name': name, 'rss': rss or '0 KB'}
        except (IOError, PermissionError, ProcessLookupError):
            pass
    return processes

def print_tree(procs, parent=0, indent=""):
    for pid, info in procs.items():
        if info['ppid'] == parent or (parent == 0 and info['ppid'] not in procs):
            print(f"{indent}├─ [{pid}] {info['name']} (State: {info['state']}, RSS: {info['rss']})")
            print_tree(procs, pid, indent + "│  ")

if __name__ == "__main__":
    print_tree(build_tree())