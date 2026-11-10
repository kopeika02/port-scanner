import socket

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((host, port))
        print(result)
        if result == 0:
            return  True
        else:
            return False

if __name__ == "__main__":
    print(check_port("127.0.0.1", 8000))
    print(check_port("127.0.0.1", 8001)) 