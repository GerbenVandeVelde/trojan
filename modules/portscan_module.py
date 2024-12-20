import socket
import nmap
import multiprocessing
import os
import time
import random

def start_server(port):
    host = '127.0.0.1'
    log_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'portscan_log.txt')

    with open(log_file, 'a') as log:
        log.write(f"Server draait op poort {port}\n")
        print(f"Server draait op poort {port}\n")  # Console output
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)
            log.write(f"Server is gestart op {host}:{port} en wacht op verbindingen...\n")

            while True:
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    log.write(f"Verbonden met {client_address}\n")
                    client_socket.sendall(b"Welkom bij de server! Stuur het geheime wachtwoord.\n")

                    try:
                        secret = client_socket.recv(1024)
                        log.write(f"Ontvangen data (in bytes): {secret}\n")

                        try:
                            secret = secret.decode('utf-8').strip()
                        except UnicodeDecodeError:
                            log.write("Fout bij het decoderen van het bericht. Verwacht tekst.\n")
                            client_socket.sendall(b"Fout bij het ontvangen van het wachtwoord.\n")
                            continue

                        if secret == "geheim":
                            client_socket.sendall(b"Goed gedaan! Het geheime bericht is: Toegang verleend!\n")
                        else:
                            client_socket.sendall(b"Fout wachtwoord! Toegang geweigerd.\n")
                    except Exception as e:
                        log.write(f"Er is een fout opgetreden: {e}\n")
                        client_socket.sendall(b"Fout bij het ontvangen van het wachtwoord.\n")

def scan_ports():
    nm = nmap.PortScanner()
    nm.scan('127.0.0.1', '9000-15000')  # Scan poorten van 9000 tot 15000
    open_ports = []
    for port in nm['127.0.0.1']['tcp']:
        if nm['127.0.0.1']['tcp'][port]['state'] == 'open':
            open_ports.append(port)
    return open_ports

def authenticate_with_server():
    host = '127.0.0.1'
    log_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'portscan_log.txt')

    with open(log_file, 'a') as log:
        open_ports = scan_ports()
        for port in open_ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                try:
                    client_socket.connect((host, port))
                    log.write(f"Verbonden met server op poort {port}\n")

                    welcome_msg = client_socket.recv(1024).decode()
                    log.write(welcome_msg)

                    client_socket.sendall(b"geheim\n")

                    secret_msg = client_socket.recv(1024).decode()
                    log.write(secret_msg)
                except Exception as e:
                    log.write(f"Fout bij verbinden met poort {port}: {e}\n")

def run():
    port = random.randint(9000, 15000)  # Dynamische poorttoewijzing
    server_process = multiprocessing.Process(target=start_server, args=(port,))
    client_process = multiprocessing.Process(target=authenticate_with_server)

    server_process.start()
    time.sleep(5)  # Wacht 5 seconden om ervoor te zorgen dat de server is opgestart
    client_process.start()

    server_process.join()
    client_process.join()

if __name__ == "__main__":
    run()
