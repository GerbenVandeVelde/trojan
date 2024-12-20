import socket

def run():
    target_ip = "127.0.0.1"
    open_ports = []
    for port in range(1, 65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    print(f"Open ports: {open_ports}")
