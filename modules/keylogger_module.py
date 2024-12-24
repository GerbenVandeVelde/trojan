import socket
import os

def simple_port_scan():
    target = "127.0.0.1"
    port_range = range(1, 1025)  # Scant poorten 1 t/m 1024
    log_file = os.path.join(os.path.dirname(__file__), 'data', 'portscan_log.txt')

    # Zorg dat de map 'data' bestaat
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    print(f"Starting port scan on {target}...")
    results = []

    for port in port_range:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Timeout instellen om sneller te scannen
            result = s.connect_ex((target, port))  # 0 betekent open
            if result == 0:
                result_line = f"Port {port} is open.\n"
                results.append(result_line)
                print(result_line.strip())  # Print naar console

    print("Port scan complete.")

    # Schrijf resultaten naar logbestand
    with open(log_file, 'w') as log:
        log.write("Port Scan Results:\n")
        log.writelines(results)

    print(f"Results have been saved to {log_file}")

if __name__ == "__main__":
    simple_port_scan()
