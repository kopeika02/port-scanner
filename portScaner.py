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
        print("can't find host:", host)
        return []
    print("Scanning")
    openPorts = []
    done = 0
    startTime = time.time()
    ports = range(start, end + 1)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda p: check_port(host, p, timeout), ports)
        for port, is_open in zip (ports, results):
            total = len(ports)
            if is_open:
                openPorts.append(port)
                print(f"({openPorts}", end="", flush=True)
            done += 1
            print(f"\r{done}/{total} ({done * 100 // total}%)", end="", flush=True)
        print()
    print("Scan take:", time.time() - startTime, "seconds")
    return openPorts

def scan_portsB(host, start, end,timeout=1, workers=100,out = False ):
    portsWithBanner = []
    openPorts = scan_ports(host, start, end,timeout, workers)
    startTime = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda p: grab_banner(host, p, timeout), openPorts)
        for port, banner in zip(openPorts, results):
            if banner is  None:
                banner = ("(No banner)")
            portsWithBanner.append((port,banner))

    print("Banners take:", time.time() - startTime, "seconds")
    if out:
        for port,banner in portsWithBanner:
            print(f"{port} : open | {' '.join(banner.split()) }")

    return portsWithBanner



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port scaner")
    parser.add_argument("host", help="host to scan")
    parser.add_argument("-s", "--start", type=int, default=1, help="First port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Last port")
    parser.add_argument("-t","--timeout",type=float,default=1,help="Time out")
    parser.add_argument("-w","--workers",type=int,default=100,help="Num of workers")
    parser.add_argument("-b","--banners",action="store_true",help="Show banners")
    args = parser.parse_args()
    if not (1 <= args.start <= args.end <= 65535):
        parser.error("ports only in 1-65535 range,start can't be greater than end")
    if args.banners:
        scan_portsB(args.host, args.start, args.end,args.timeout, args.workers,True)
    else:
        print(f"\n{scan_ports(args.host, args.start, args.end,args.timeout, args.workers)}\n")
