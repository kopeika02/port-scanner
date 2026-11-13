import socket
import time
from concurrent.futures import ThreadPoolExecutor
from banner import grab_banner

def check_port(host, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        return result == 0

def scan_ports(host, start, end,timeout=1, workers=100 ):
    print("Сканирование портов")
    openPorts = []
    startTime = time.time()
    ports = range(start, end + 1)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda p: check_port(host, p, timeout), ports)
        for port, is_open in zip (ports, results):
            if is_open:
                openPorts.append(port)
    print("Сканирование Заняло:", time.time() - startTime, "сек")
    return openPorts

def scan_portsB(host, start, end,timeout=1, workers=100,out = False ):
    banners = []
    openPorts = scan_ports(host, start, end,timeout, workers)
    startTime = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda p: grab_banner(host, p, timeout), openPorts)
        for port, banner in zip(openPorts, results):
            if banner is  None:
                banner = ("(баннера нет)")
            banners.append(banner)

    portsWithBanner = (list(zip(openPorts,banners)))
    print("Баннеры Заняли:", time.time() - startTime, "сек")
    if out:
        for port,banner in portsWithBanner:
            print(f"{port} : открыт | {' '.join(banner.split()) }")

    return portsWithBanner



if __name__ == "__main__":
    #scan_ports("localhost", 1,1024)
    scan_portsB("localhost", 1, 1024, workers=1024,out = True)
