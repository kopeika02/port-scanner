import socket
import time
from concurrent.futures import ThreadPoolExecutor
from banner import grab_banner
import argparse

def check_port(host, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0

def scan_ports(host, start, end,timeout=1, workers=100 ):
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        print("Не удалось найти хост:", host)
        return []
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
    portsWithBanner = []
    openPorts = scan_ports(host, start, end,timeout, workers)
    startTime = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda p: grab_banner(host, p, timeout), openPorts)
        for port, banner in zip(openPorts, results):
            if banner is  None:
                banner = ("(баннера нет)")
            portsWithBanner.append((port,banner))

    print("Баннеры Заняли:", time.time() - startTime, "сек")
    if out:
        for port,banner in portsWithBanner:
            print(f"{port} : открыт | {' '.join(banner.split()) }")

    return portsWithBanner



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сканер портов")
    parser.add_argument("host", help="адрес для сканирования")
    parser.add_argument("-s", "--start", type=int, default=1, help="первый порт")
    parser.add_argument("-e", "--end", type=int, default=1024, help="последний порт")
    parser.add_argument("-t","--timeout",type=float,default=1,help="Время ожидания")
    parser.add_argument("-w","--workers",type=int,default=100,help="Количество потоков")
    parser.add_argument("-b","--banners",action="store_true",help="Показ банеров")
    args = parser.parse_args()
    if not (1 <= args.start <= args.end <= 65535):
        parser.error("порты должны быть в диапазоне 1-65535, и start не больше end")
    if args.banners:
        scan_portsB(args.host, args.start, args.end,args.timeout, args.workers,True)
    else:
        print(scan_ports(args.host, args.start, args.end,args.timeout, args.workers))
