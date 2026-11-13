import socket

def grab_banner(host, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            try:
                data = s.recv(1024)
            except socket.timeout:
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                data = s.recv(1024)
    except OSError:
        return None

    if not data:
        return None
    return data.decode("utf-8", errors="ignore").strip()

if __name__ == "__main__":
    print(grab_banner("localhost", 8000))