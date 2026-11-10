import socket
import time
from concurrent.futures import ThreadPoolExecutor

def check_port(host, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        return result == 0

def scan_ports(host, start, end,timeout=1, workers=100 ):
    print("Scanning ports...")
    openPorts = []
    startTime = time.time()
    ports = range(start, end + 1)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda p: check_port(host, p, timeout), ports)
        for port, is_open in zip (ports, results):
            if is_open:
                openPorts.append(port)
    print("Заняло:", time.time() - startTime, "сек")
    return openPorts

if __name__ == "__main__":
    print(scan_ports("192.168.0.1", 1, 1024))
