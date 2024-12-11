import socket

def run(target="127.0.0.1", ports=range(20, 1025)):
    """Scan open ports on a target."""
    open_ports = []
    for port in ports:
        try:
            with socket.create_connection((target, port), timeout=1):
                open_ports.append(port)
        except:
            continue
    return {"target": target, "open_ports": open_ports}
