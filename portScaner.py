import socket
import time

def check_port(host, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        return result == 0

def scan_ports(host, start, end, ):
    print("Scanning ports...")
    openPorts = []
    startTime = time.time()
    for port in range(start, end+1):
        is_open = check_port(host, port)
        if is_open:
            openPorts.append(port)
            print(port, 'open')

    print("Заняло:", time.time() - startTime, "сек")
    return openPorts

if __name__ == "__main__":
    print(scan_ports("127.0.0.1", 1, 4096))
